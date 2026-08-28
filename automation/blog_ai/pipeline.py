from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import socket
import tempfile
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from openai import OpenAI

from .config import Settings, load_feeds, load_ideas
from .image import save_cover
from .models import Idea, PipelineResult
from .network import normalized_url
from .openai_client import OpenAIWriter
from .privacy import PrivacyGate
from .quality import QualityGate
from .render import render_artifacts
from .site_index import load_public_title_index
from .sources import fetch_sources, hydrate_sources


@dataclass
class RunState:
    generated_count: int = 0


def _output_dir(settings: Settings, repo_root: Path) -> Path:
    return settings.output_dir if settings.output_dir.is_absolute() else repo_root / settings.output_dir


def _privacy_findings(gate: PrivacyGate, draft, sources) -> list:
    values = [
        (draft.title, "title"),
        (draft.description, "description"),
        (draft.body_markdown, "body"),
        (draft.image_prompt, "image_prompt"),
        (draft.image_alt, "image_alt"),
    ]
    values.extend((source.excerpt, "source_excerpt") for source in sources)
    return [finding for text, label in values for finding in gate.check_text(text, label)]


def run_pipeline(
    settings: Settings,
    *,
    writer: OpenAIWriter,
    repo_root: Path = Path("."),
    feeds=None,
    ideas=None,
    titles=None,
    source_fetcher=fetch_sources,
    source_hydrator=hydrate_sources,
    image_saver=save_cover,
    repository_validator=None,
    generated_at: datetime | None = None,
    skip_image: bool = False,
    dry_run: bool = False,
    state: RunState | None = None,
    pr_body_path: Path | None = None,
) -> PipelineResult:
    state = state or RunState()
    if state.generated_count:
        raise RuntimeError("only one generated post is allowed per run")

    repo_root = repo_root.resolve()
    output_dir = _output_dir(settings, repo_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    feeds = load_feeds(repo_root / "automation/config/feeds.yml") if feeds is None else feeds
    ideas = load_ideas(repo_root / "automation/config/ideas.yml") if ideas is None else ideas
    titles = load_public_title_index(
        repo_root / "_posts", repo_root / "_data/legacy_channel_allowlist.yml"
    ) if titles is None else titles
    generated_at = generated_at or datetime.now(timezone.utc)

    try:
        candidates = source_fetcher(feeds, ideas, max_candidates=settings.max_candidates)
    except Exception:
        return PipelineResult(status="rejected", reason="source_fetch")
    if not candidates:
        return PipelineResult(status="no_candidate", reason="no_public_sources")

    try:
        selected = writer.select_topic(candidates, titles, ideas)
    except Exception:
        return PipelineResult(status="rejected", reason="topic_selection")
    if not selected.publish:
        return PipelineResult(status="no_candidate", reason="selector_rejected")

    selected_urls = {str(url) for url in selected.source_urls}
    selected_sources = [source for source in candidates if str(source.url) in selected_urls]
    allowed_hosts = {urlsplit(str(source.url)).hostname for source in selected_sources}
    allowed_hosts.discard(None)
    try:
        hydrated = source_hydrator(selected_sources, allowed_hosts)
        draft = writer.generate_article(selected, hydrated)
    except Exception:
        return PipelineResult(status="rejected", reason="article_generation")

    allowed_urls = {normalized_url(str(source.url)) for source in hydrated}
    privacy_gate = PrivacyGate(allowed_urls)
    if _privacy_findings(privacy_gate, draft, hydrated):
        return PipelineResult(status="rejected", reason="privacy_gate")
    if QualityGate().validate(draft, hydrated, titles):
        return PipelineResult(status="rejected", reason="quality_gate")

    with tempfile.TemporaryDirectory(prefix="stage-", dir=output_dir) as stage_name:
        stage = Path(stage_name)
        file_date = generated_at.astimezone(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
        image_name = f"{file_date}-{draft.slug}.webp"
        staged_image = stage / "assets/images/posts" / image_name
        try:
            if skip_image:
                raw_image = (repo_root / "assets/images/site/tech-default.webp").read_bytes()
            else:
                raw_image = writer.generate_image(draft.image_prompt)
            image_info = image_saver(raw_image, staged_image)
        except Exception:
            return PipelineResult(status="rejected", reason="image_generation")

        staged_pr_body = stage / "ai-draft-pr-body.md"
        try:
            artifacts = render_artifacts(
                topic=selected,
                draft=draft,
                sources=hydrated,
                image_info=image_info,
                text_model=settings.text_model,
                image_model=settings.image_model if not skip_image else "checked-in-neutral-cover",
                generated_at=generated_at,
                validation_summaries=["privacy:pass", "quality:pass", "image:pass"],
                posts_dir=stage / "_posts",
                output_dir=stage / "output",
                pr_body_path=staged_pr_body,
                privacy_gate=privacy_gate,
            )
        except Exception:
            return PipelineResult(status="rejected", reason="render_gate")

        public_image_name = artifacts.public_image_path.name
        if dry_run:
            preview_dir = output_dir / "preview"
            preview_dir.mkdir(parents=True, exist_ok=True)
            post_path = preview_dir / artifacts.post_path.name
            image_path = preview_dir / public_image_name
            shutil.copy2(artifacts.post_path, post_path)
            shutil.copy2(staged_image, image_path)
        else:
            post_path = repo_root / "_posts" / artifacts.post_path.name
            image_path = repo_root / "assets/images/posts" / public_image_name
            if post_path.exists() or image_path.exists():
                return PipelineResult(status="rejected", reason="output_collision")
            post_path.parent.mkdir(parents=True, exist_ok=True)
            image_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(artifacts.post_path, post_path)
            shutil.move(staged_image, image_path)
            try:
                if repository_validator:
                    repository_validator(post_path, image_path)
            except Exception:
                post_path.unlink(missing_ok=True)
                image_path.unlink(missing_ok=True)
                return PipelineResult(status="rejected", reason="repository_validation")

        packet_path = output_dir / "research.json"
        final_pr_body = pr_body_path or output_dir / "ai-draft-pr-body.md"
        final_pr_body.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(artifacts.packet_path, packet_path)
        shutil.copy2(staged_pr_body, final_pr_body)
        state.generated_count += 1
        return PipelineResult(
            status="generated",
            post_path=post_path,
            image_path=image_path,
            packet_path=packet_path,
            pr_body_path=final_pr_body,
        )


def _cli() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--idea-title", default="")
    parser.add_argument("--idea-url", default="")
    parser.add_argument("--skip-image", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    settings = Settings.from_env()
    ideas = load_ideas(Path("automation/config/ideas.yml"))
    if args.idea_url and urlsplit(args.idea_url).scheme.lower() != "https":
        result = PipelineResult(status="rejected", reason="workflow_url")
    else:
        if args.idea_title or args.idea_url:
            ideas.append(Idea(title=args.idea_title or "Workflow idea", url=args.idea_url or None))
        client = OpenAI(api_key=settings.api_key)
        writer = OpenAIWriter(
            client,
            settings.text_model,
            Path("automation/prompts"),
            image_model=settings.image_model,
        )
        result = run_pipeline(
            settings,
            writer=writer,
            ideas=ideas,
            skip_image=args.skip_image,
            dry_run=args.dry_run,
            pr_body_path=Path("/tmp/ai-draft-pr-body.md"),
        )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(result.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print(result.status)
    return 0 if result.status in {"generated", "no_candidate"} else 2


if __name__ == "__main__":
    raise SystemExit(_cli())
