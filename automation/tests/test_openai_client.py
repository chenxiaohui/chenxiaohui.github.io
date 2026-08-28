from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from automation.blog_ai.models import ArticleDraft, SourceItem, SourceNote, TopicScore
from automation.blog_ai.openai_client import OpenAIWriter


class FakeResponses:
    def __init__(self, parsed):
        self.parsed = parsed
        self.calls = []

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            status="completed",
            id="resp_public",
            usage=SimpleNamespace(input_tokens=10, output_tokens=5),
            output=[SimpleNamespace(type="message", content=[SimpleNamespace(type="output_text", parsed=self.parsed)])],
        )


class FakeClient:
    def __init__(self, parsed):
        self.responses = FakeResponses(parsed)


def source():
    return SourceItem(
        title="Public release",
        url="https://example.com/release",
        published_at=datetime(2026, 8, 27, tzinfo=timezone.utc),
        excerpt="Public facts only",
        content="Documented public content",
    )


def topic():
    return TopicScore(
        source_urls=["https://example.com/release"],
        title="Public systems topic",
        angle="Explain the documented mechanism",
        related_titles=[],
        topic="系统",
        relevance=4,
        source_quality=5,
        viewpoint_space=4,
        duplicate_risk=1,
        publish=True,
    )


def draft(**updates):
    values = dict(
        title="Public systems article",
        slug="public-systems-article",
        description="A concise public-source description",
        topic="系统",
        body_markdown="公开系统机制与取舍。" * 180,
        source_urls=["https://example.com/release"],
        source_notes=[SourceNote(url="https://example.com/release", facts=["Documented public content"])],
        source_conflicts=[],
        image_prompt="3:2 editorial systems illustration without text",
        image_alt="抽象的软件系统节点与数据流插画",
        review_facts=["Confirm the documented mechanism"],
    )
    values.update(updates)
    return ArticleDraft(**values)


def test_select_topic_sends_only_public_packet(tmp_path: Path):
    (tmp_path / "topic_selection.md").write_text("Select from the packet only.", encoding="utf-8")
    score = TopicScore(
        source_urls=["https://example.com/release"],
        title="Public systems topic",
        angle="Explain the documented mechanism",
        related_titles=["Existing public title"],
        topic="系统",
        relevance=4,
        source_quality=5,
        viewpoint_space=4,
        duplicate_risk=1,
        publish=True,
    )
    client = FakeClient(score)
    writer = OpenAIWriter(client, "gpt-5.6-terra", tmp_path)

    result = writer.select_topic([source()], ["Existing public title"], [{"title": "Idea", "note": "Public note"}])

    call = client.responses.calls[0]
    assert result == score
    assert call["text_format"] is TopicScore
    assert call["store"] is False
    assert "BODY_MUST_NOT_LEAK" not in call["input"]


def test_generate_article_uses_only_referenced_sources(tmp_path: Path):
    (tmp_path / "article_generation.md").write_text("Use packet facts only.", encoding="utf-8")
    client = FakeClient(draft())
    writer = OpenAIWriter(client, "gpt-5.6-terra", tmp_path)
    unused = source().model_copy(update={"url": "https://example.com/unused", "title": "Unused"})

    result = writer.generate_article(topic(), [source(), unused])

    call = client.responses.calls[0]
    assert result.slug == "public-systems-article"
    assert call["text_format"] is ArticleDraft
    assert call["store"] is False
    assert "https://example.com/unused" not in call["input"]


@pytest.mark.parametrize(
    "invalid_draft",
    [
        draft(source_urls=["https://outside.example/fact"]),
        draft(slug="Invalid Slug"),
        draft(body_markdown="太短"),
    ],
)
def test_generate_article_rejects_invalid_output(tmp_path: Path, invalid_draft):
    (tmp_path / "article_generation.md").write_text("Use packet facts only.", encoding="utf-8")
    writer = OpenAIWriter(FakeClient(invalid_draft), "gpt-5.6-terra", tmp_path)
    with pytest.raises(RuntimeError):
        writer.generate_article(topic(), [source()])
