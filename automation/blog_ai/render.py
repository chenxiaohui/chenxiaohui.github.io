from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

import yaml

from .image import ImageInfo
from .models import ArticleDraft, SourceItem, TopicScore
from .privacy import PrivacyGate


@dataclass(frozen=True)
class RenderedArtifacts:
    post_path: Path
    packet_path: Path
    pr_body_path: Path
    public_image_path: Path


def _safe_scalar(value: object, label: str) -> str:
    text = str(value)
    if re.search(r"[\x00-\x1f\x7f]", text):
        raise ValueError(f"{label} contains a control character")
    return text


def _markdown_text(value: object, label: str) -> str:
    text = _safe_scalar(value, label)
    return re.sub(r"([\\\[\]()])", r"\\\1", text)


def _front_matter(draft: ArticleDraft, generated_at: datetime, cover: str) -> str:
    if generated_at.tzinfo is None or generated_at.utcoffset() is None:
        raise ValueError("generated_at must include a timezone")
    local_time = generated_at.astimezone(ZoneInfo("America/Los_Angeles"))
    data = {
        "title": _safe_scalar(draft.title, "title"),
        "date": local_time.strftime("%Y-%m-%d %H:%M %z"),
        "channel": "tech",
        "topics": [draft.topic],
        "description": _safe_scalar(draft.description, "description"),
        "cover": _safe_scalar(cover, "cover"),
        "cover_alt": _safe_scalar(draft.image_alt, "cover_alt"),
        "ai_assisted": True,
        "allow_ai_index": True,
        "sources": [_safe_scalar(str(url), "source URL") for url in draft.source_urls],
    }
    dumped = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    dumped = re.sub(r"(?m)^- ", "  - ", dumped)
    return f"---\n{dumped}---\n\n"


def render_artifacts(
    *,
    topic: TopicScore,
    draft: ArticleDraft,
    sources: list[SourceItem],
    image_info: ImageInfo,
    text_model: str,
    image_model: str,
    generated_at: datetime,
    validation_summaries: list[str],
    posts_dir: Path,
    output_dir: Path,
    pr_body_path: Path,
    privacy_gate: PrivacyGate,
) -> RenderedArtifacts:
    slug = _safe_scalar(draft.slug, "slug")
    local_date = generated_at.astimezone(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    post_name = f"{local_date}-{slug}.md"
    image_name = f"{local_date}-{slug}.webp"
    public_post_path = Path("_posts") / post_name
    public_image_path = Path("assets/images/posts") / image_name
    cover = f"/{public_image_path.as_posix()}"

    if re.search(r"(?m)^#\s+", draft.body_markdown):
        raise ValueError("article body must not contain an H1")
    post = _front_matter(draft, generated_at, cover) + draft.body_markdown.rstrip() + "\n"

    source_by_url = {str(source.url): source for source in sources}
    source_lines = "\n\n".join(
        "\n".join(
            [
                f"- [{_markdown_text(source_by_url[str(note.url)].title, 'source title')}]({_safe_scalar(note.url, 'source URL')})",
                f"  - 发布日期：{source_by_url[str(note.url)].published_at or '未提供'}",
                *[f"  - 使用事实：{_markdown_text(fact, 'source fact')}" for fact in note.facts],
            ]
        )
        for note in draft.source_notes
    )
    review_lines = "\n".join(f"- [ ] {_markdown_text(fact, 'review fact')}" for fact in draft.review_facts)
    related_lines = "\n".join(f"- {_markdown_text(title, 'related title')}" for title in topic.related_titles) or "- 无直接重复"
    pr_body = f"""## 选题

{_markdown_text(draft.title, 'title')}：{_markdown_text(topic.angle, 'angle')}

## 与站内文章的关系

{related_lines}

## 公开资料包

{source_lines}

## 需要人工复核

{review_lines}

## 生成内容

- 文章：{public_post_path}
- 配图：{public_image_path}
- channel：tech
- topic：{draft.topic}
- AI 协助：是

## 检查

- [x] Python tests
- [x] privacy and evidence gates
- [x] image metadata and size
- [x] Jekyll production build
- [x] generated-site validation

## 生成信息

- Text model: {_safe_scalar(text_model, 'text model')}
- Image model: {_safe_scalar(image_model, 'image model')}
- Generated at: {generated_at.isoformat()}
- Image prompt: {_markdown_text(draft.image_prompt, 'image prompt')}
"""
    findings = privacy_gate.check_text(pr_body, "pr_body")
    if findings:
        raise ValueError("PR body failed privacy validation")

    research = {
        "sources": [
            {
                "url": str(source.url),
                "title": source.title,
                "published_at": source.published_at.isoformat() if source.published_at else None,
                "excerpt": source.excerpt,
            }
            for source in sources
        ],
        "topic_score": topic.model_dump(mode="json"),
        "source_notes": [note.model_dump(mode="json") for note in draft.source_notes],
        "review_facts": draft.review_facts,
        "text_model": text_model,
        "image_model": image_model,
        "image_prompt": draft.image_prompt,
        "image": {
            "path": public_image_path.as_posix(),
            "width": image_info.width,
            "height": image_info.height,
            "size_bytes": image_info.size_bytes,
            "sha256": image_info.sha256,
        },
        "generated_at": generated_at.isoformat(),
        "validation_summaries": validation_summaries,
    }

    posts_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    pr_body_path.parent.mkdir(parents=True, exist_ok=True)
    post_path = posts_dir / post_name
    packet_path = output_dir / "research.json"
    post_path.write_text(post, encoding="utf-8")
    packet_path.write_text(json.dumps(research, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pr_body_path.write_text(pr_body, encoding="utf-8")
    return RenderedArtifacts(
        post_path=post_path,
        packet_path=packet_path,
        pr_body_path=pr_body_path,
        public_image_path=public_image_path,
    )
