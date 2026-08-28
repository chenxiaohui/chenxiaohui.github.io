#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import re
import subprocess
import sys

from PIL import Image
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
import yaml

from automation.blog_ai.models import ArticleDraft, SourceItem, SourceNote, TopicScore
from automation.blog_ai.privacy import PrivacyGate
from automation.blog_ai.quality import QualityGate
from automation.blog_ai.site_index import load_public_title_index


class GeneratedFrontMatter(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    date: str
    channel: str
    topics: list[str] = Field(min_length=1)
    description: str
    cover: str
    cover_alt: str
    ai_assisted: bool
    allow_ai_index: bool
    sources: list[HttpUrl] = Field(min_length=1)


def read_post(path: Path) -> tuple[GeneratedFrontMatter, str, str]:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n\n(.*)\Z", raw, re.DOTALL)
    if not match:
        raise ValueError("post format")
    front_raw, body = match.groups()
    data = GeneratedFrontMatter.model_validate(yaml.safe_load(front_raw))
    if data.channel != "tech" or any(topic not in {"AI", "系统", "推荐", "工具"} for topic in data.topics):
        raise ValueError("channel or topic")
    if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2} [+-]\d{4}$", data.date):
        raise ValueError("date timezone")
    if not data.ai_assisted or not data.allow_ai_index:
        raise ValueError("AI flags")
    return data, body, front_raw


def git_added_files() -> set[str]:
    tracked = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return set(tracked + untracked)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage FAIL")
        return 1
    post_path = Path(sys.argv[1])
    image_path = Path(sys.argv[2])
    checks: list[tuple[str, bool]] = []

    try:
        front, body, front_raw = read_post(post_path)
        checks.append(("schema", True))
    except Exception:
        checks.append(("schema", False))
        front = body = front_raw = None

    packet_path = Path("automation/output/research.json")
    try:
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        topic = TopicScore.model_validate(packet["topic_score"])
        notes = [SourceNote.model_validate(note) for note in packet["source_notes"]]
        note_facts = {str(note.url): " ".join(note.facts) for note in notes}
        sources = [
            SourceItem(
                title=item["title"],
                url=item["url"],
                published_at=datetime.fromisoformat(item["published_at"]) if item["published_at"] else None,
                excerpt=item["excerpt"],
                content=f"{item['excerpt']} {note_facts.get(item['url'], '')}",
            )
            for item in packet["sources"]
        ]
    except Exception:
        packet = None
        topic = None
        notes = []
        sources = []

    if front is not None and packet is not None:
        allowed_urls = {str(url) for url in front.sources}
        gate = PrivacyGate(allowed_urls)
        privacy_findings = []
        for text, label in [
            (front.title, "title"),
            (front.description, "description"),
            (body, "body"),
            (front_raw, "front_matter"),
            (packet["image_prompt"], "image_prompt"),
        ]:
            privacy_findings.extend(gate.check_text(text, label))
        pr_body = Path("/tmp/ai-draft-pr-body.md")
        if pr_body.exists():
            privacy_findings.extend(gate.check_text(pr_body.read_text(encoding="utf-8"), "pr_body"))
        checks.append(("privacy", not privacy_findings))

        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post_path.stem)
        draft = ArticleDraft(
            title=front.title,
            slug=slug,
            description=front.description,
            topic=front.topics[0],
            body_markdown=body.rstrip(),
            source_urls=front.sources,
            source_notes=notes,
            source_conflicts=[],
            image_prompt=packet["image_prompt"],
            image_alt=front.cover_alt,
            review_facts=packet["review_facts"],
        )
        titles = load_public_title_index(Path("_posts"), Path("_data/legacy_channel_allowlist.yml"))
        if front.title in titles:
            titles.remove(front.title)
        checks.append(("quality", not QualityGate().validate(draft, sources, titles)))
    else:
        checks.extend([("privacy", False), ("quality", False)])

    try:
        with Image.open(image_path) as image:
            image_ok = (
                image.format == "WEBP"
                and image.mode == "RGB"
                and image.size == (1536, 1024)
                and not image.getexif()
                and not ({"exif", "icc_profile", "xmp"} & set(image.info))
                and image_path.stat().st_size <= 450 * 1024
            )
        checks.append(("image", image_ok))
    except Exception:
        checks.append(("image", False))

    try:
        added = git_added_files()
        generated = {
            path for path in added if path.startswith("_posts/") or path.startswith("assets/images/posts/")
        }
        expected = {post_path.as_posix(), image_path.as_posix()}
        checks.append(("git_surface", generated == expected))
    except Exception:
        checks.append(("git_surface", False))

    for name, passed in checks:
        print(f"{name} {'PASS' if passed else 'FAIL'}")
    passed_count = sum(passed for _name, passed in checks)
    print(f"{passed_count} passed, {len(checks) - passed_count} failed")
    return 0 if all(passed for _name, passed in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
