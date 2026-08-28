from datetime import datetime, timezone
from pathlib import Path

import pytest

from automation.blog_ai.config import Settings
from automation.blog_ai.image import ImageInfo
from automation.blog_ai.models import ArticleDraft, SourceItem, SourceNote, TopicScore
from automation.blog_ai.pipeline import RunState, run_pipeline


URL = "https://example.com/source"


def source():
    return SourceItem(
        title="Public source",
        url=URL,
        published_at=None,
        excerpt="Documented public mechanism and system tradeoff",
        content="Documented public mechanism and system tradeoff with design constraints.",
    )


def topic(publish=True):
    return TopicScore(
        source_urls=[URL],
        title="Public systems topic",
        angle="Explain the public mechanism",
        related_titles=[],
        topic="系统",
        relevance=5,
        source_quality=5,
        viewpoint_space=4,
        duplicate_risk=1,
        publish=publish,
    )


def article(body=None):
    body = body or "\n\n".join(
        [
            "## 机制",
            "公开系统机制与设计取舍。" * 50,
            "## 边界",
            "公开资料说明系统边界与约束。" * 50,
            "## 开放问题",
            "仍需根据公开文档核对机制与限制。" * 50,
        ]
    )
    return ArticleDraft(
        title="Public systems article",
        slug="public-systems-article",
        description="A concise public-source description",
        topic="系统",
        body_markdown=body,
        source_urls=[URL],
        source_notes=[SourceNote(url=URL, facts=["Documented public mechanism and system tradeoff"])],
        source_conflicts=[],
        image_prompt="abstract public systems illustration",
        image_alt="抽象的软件系统节点与数据流插画",
        review_facts=[],
    )


class Writer:
    def __init__(self, selected=None, generated=None, image_error=False):
        self.selected = selected or topic()
        self.generated = generated or article()
        self.image_error = image_error

    def select_topic(self, sources, titles, ideas):
        return self.selected

    def generate_article(self, selected, sources):
        return self.generated

    def generate_image(self, prompt):
        if self.image_error:
            raise ValueError("image failed")
        return b"raw-image"


def settings(tmp_path):
    return Settings(api_key="test", text_model="text-model", image_model="image-model", output_dir=tmp_path / "output")


def fake_saver(raw, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"webp")
    return ImageInfo(path=target, width=1536, height=1024, size_bytes=4, sha256="abcd")


def run(tmp_path, *, candidates=None, writer=None, validator=lambda post, image: None, state=None):
    return run_pipeline(
        settings(tmp_path),
        writer=writer or Writer(),
        repo_root=tmp_path,
        feeds=[],
        ideas=[],
        titles=[],
        source_fetcher=lambda *args, **kwargs: list(candidates or []),
        source_hydrator=lambda items, *args, **kwargs: items,
        image_saver=fake_saver,
        repository_validator=validator,
        generated_at=datetime(2026, 8, 28, 16, 0, tzinfo=timezone.utc),
        state=state,
    )


def test_no_candidates_creates_no_files(tmp_path):
    result = run(tmp_path)
    assert result.status == "no_candidate"
    assert not (tmp_path / "_posts").exists()


def test_selector_rejection_creates_no_files(tmp_path):
    result = run(tmp_path, candidates=[source()], writer=Writer(selected=topic(False)))
    assert result.status == "no_candidate"
    assert not (tmp_path / "_posts").exists()


def test_privacy_finding_rejects_and_cleans_staging(tmp_path):
    body = article().body_markdown + "\n\n我们线上使用内部代码。"
    result = run(tmp_path, candidates=[source()], writer=Writer(generated=article(body)))
    assert result.status == "rejected"
    assert result.reason == "privacy_gate"
    assert not (tmp_path / "_posts").exists()
    assert not list((tmp_path / "output").glob("stage-*"))


def test_image_failure_leaves_no_post(tmp_path):
    result = run(tmp_path, candidates=[source()], writer=Writer(image_error=True))
    assert result.status == "rejected"
    assert not (tmp_path / "_posts").exists()


def test_happy_path_creates_exactly_one_post_and_image_and_validates(tmp_path):
    calls = []
    result = run(tmp_path, candidates=[source()], validator=lambda post, image: calls.append((post, image)))
    assert result.status == "generated"
    assert len(list((tmp_path / "_posts").glob("*.md"))) == 1
    assert len(list((tmp_path / "assets/images/posts").glob("*.webp"))) == 1
    assert len(calls) == 1


def test_second_generation_in_same_run_is_a_hard_failure(tmp_path):
    state = RunState()
    assert run(tmp_path, candidates=[source()], state=state).status == "generated"
    with pytest.raises(RuntimeError, match="one generated post"):
        run(tmp_path, candidates=[source()], state=state)
