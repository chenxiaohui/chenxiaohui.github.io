from datetime import datetime, timezone
from pathlib import Path

from automation.blog_ai.image import ImageInfo
from automation.blog_ai.models import ArticleDraft, SourceItem, SourceNote, TopicScore
from automation.blog_ai.privacy import PrivacyGate
from automation.blog_ai.render import render_artifacts


def test_renders_exact_front_matter_and_review_artifacts(tmp_path: Path):
    generated_at = datetime(2026, 8, 28, 16, 0, tzinfo=timezone.utc)
    sources = [
        SourceItem(title="Source A", url="https://example.com/source-a", published_at=None, excerpt="Fact A", content="Fact A content"),
        SourceItem(title="Source B", url="https://example.com/source-b", published_at=None, excerpt="Fact B", content="Fact B content"),
    ]
    topic = TopicScore(
        source_urls=[source.url for source in sources],
        title="A public systems article",
        angle="Explain the public mechanism",
        related_titles=[],
        topic="系统",
        relevance=5,
        source_quality=5,
        viewpoint_space=4,
        duplicate_risk=1,
        publish=True,
    )
    draft = ArticleDraft(
        title="A public systems article",
        slug="public-systems-article",
        description="A concise public-source description",
        topic="系统",
        body_markdown="## Mechanism\n\nPublic body.\n\n## Tradeoff\n\nPublic tradeoff.\n\n## Limits\n\nPublic limits.",
        source_urls=[source.url for source in sources],
        source_notes=[
            SourceNote(url="https://example.com/source-a", facts=["Fact A"]),
            SourceNote(url="https://example.com/source-b", facts=["Fact B"]),
        ],
        source_conflicts=[],
        image_prompt="abstract public system",
        image_alt="抽象的软件系统节点与数据流插画",
        review_facts=["Confirm source dates"],
    )
    image_path = tmp_path / "cover.webp"
    image_path.write_bytes(b"webp")
    image = ImageInfo(path=image_path, width=1536, height=1024, size_bytes=4, sha256="abcd")
    posts_dir = tmp_path / "posts"
    output_dir = tmp_path / "output"
    pr_body_path = tmp_path / "pr-body.md"

    artifacts = render_artifacts(
        topic=topic,
        draft=draft,
        sources=sources,
        image_info=image,
        text_model="gpt-5.6-terra",
        image_model="gpt-image-2",
        generated_at=generated_at,
        validation_summaries=["privacy:pass", "quality:pass"],
        posts_dir=posts_dir,
        output_dir=output_dir,
        pr_body_path=pr_body_path,
        privacy_gate=PrivacyGate({str(source.url) for source in sources}),
    )

    expected_front_matter = """---
title: A public systems article
date: 2026-08-28 09:00 -0700
channel: tech
topics:
  - 系统
description: A concise public-source description
cover: /assets/images/posts/2026-08-28-public-systems-article.webp
cover_alt: 抽象的软件系统节点与数据流插画
ai_assisted: true
allow_ai_index: true
sources:
  - https://example.com/source-a
  - https://example.com/source-b
---

"""
    rendered = artifacts.post_path.read_text(encoding="utf-8")
    assert rendered.startswith(expected_front_matter)
    assert rendered.endswith(draft.body_markdown + "\n")
    assert not any(line.startswith("# ") for line in rendered.splitlines())
    assert "gpt-5.6" not in rendered
    assert artifacts.packet_path == output_dir / "research.json"
    assert "## 公开资料包" in pr_body_path.read_text(encoding="utf-8")
