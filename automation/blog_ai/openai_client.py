from __future__ import annotations

import base64
import json
from pathlib import Path
import re
from typing import TypeVar

from pydantic import BaseModel

from .models import ArticleDraft, SourceItem, TopicScore


ModelType = TypeVar("ModelType", bound=BaseModel)


def parsed_output(response, expected_type: type[ModelType]) -> ModelType:
    values = [
        item.parsed
        for output in response.output
        if output.type == "message"
        for item in output.content
        if item.type == "output_text" and item.parsed is not None
    ]
    if len(values) != 1 or not isinstance(values[0], expected_type):
        raise RuntimeError("missing structured response")
    return values[0]


class OpenAIWriter:
    def __init__(self, client, text_model: str, prompt_dir: Path, image_model: str = "gpt-image-2"):
        self.client = client
        self.text_model = text_model
        self.image_model = image_model
        self.prompt_dir = prompt_dir

    def _prompt(self, name: str) -> str:
        return (self.prompt_dir / name).read_text(encoding="utf-8")

    def select_topic(self, sources: list[SourceItem], titles: list[str], ideas: list) -> TopicScore:
        idea_packet = [idea.model_dump(mode="json") if hasattr(idea, "model_dump") else dict(idea) for idea in ideas]
        research_json = json.dumps(
            {
                "sources": [source.model_dump(mode="json") for source in sources],
                "existing_titles": list(titles),
                "ideas": idea_packet,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        response = self.client.responses.parse(
            model=self.text_model,
            instructions=self._prompt("topic_selection.md"),
            input=research_json,
            text_format=TopicScore,
            max_output_tokens=1_200,
            store=False,
        )
        if response.status != "completed":
            raise RuntimeError("topic selection did not complete")
        topic = parsed_output(response, TopicScore)
        packet_urls = {str(source.url) for source in sources}
        if not {str(url) for url in topic.source_urls}.issubset(packet_urls):
            raise RuntimeError("topic referenced a URL outside the source packet")
        if not set(topic.related_titles).issubset(set(titles)):
            raise RuntimeError("topic referenced a title outside the public index")
        return topic

    def generate_article(self, topic: TopicScore, sources: list[SourceItem]) -> ArticleDraft:
        selected_urls = {str(url) for url in topic.source_urls}
        selected_sources = [source for source in sources if str(source.url) in selected_urls]
        if {str(source.url) for source in selected_sources} != selected_urls:
            raise RuntimeError("selected source is missing from the hydrated packet")
        research_json = json.dumps(
            {
                "topic": topic.model_dump(mode="json"),
                "sources": [source.model_dump(mode="json") for source in selected_sources],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        response = self.client.responses.parse(
            model=self.text_model,
            instructions=self._prompt("article_generation.md"),
            input=research_json,
            text_format=ArticleDraft,
            max_output_tokens=6_000,
            store=False,
        )
        if response.status != "completed":
            raise RuntimeError("article generation did not complete")
        draft = parsed_output(response, ArticleDraft)
        draft_urls = {str(url) for url in draft.source_urls}
        note_urls = {str(note.url) for note in draft.source_notes}
        if draft_urls != selected_urls or note_urls != selected_urls:
            raise RuntimeError("article sources do not match the selected packet")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", draft.slug):
            raise RuntimeError("article slug is invalid")
        chinese_characters = len(re.findall(r"[\u3400-\u9fff]", draft.body_markdown))
        if not 1_200 <= chinese_characters <= 2_500:
            raise RuntimeError("article body length is invalid")
        if draft.topic != topic.topic:
            raise RuntimeError("article topic does not match selection")
        if draft.source_conflicts:
            raise RuntimeError("article contains unresolved source conflicts")
        return draft

    def generate_image(self, prompt: str) -> bytes:
        full_prompt = f"{self._prompt('image_generation.md').strip()}\n\n{prompt.strip()}"
        result = self.client.images.generate(
            model=self.image_model,
            prompt=full_prompt,
            size="1536x1024",
            quality="medium",
        )
        if len(result.data) != 1 or not result.data[0].b64_json:
            raise RuntimeError("image response is missing base64 data")
        try:
            return base64.b64decode(result.data[0].b64_json, validate=True)
        except (ValueError, TypeError) as exc:
            raise RuntimeError("image response contains invalid base64") from exc
