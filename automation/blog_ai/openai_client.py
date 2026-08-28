from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from .models import SourceItem, TopicScore


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
