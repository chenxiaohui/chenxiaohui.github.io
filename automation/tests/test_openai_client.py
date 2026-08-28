from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from automation.blog_ai.models import SourceItem, TopicScore
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
