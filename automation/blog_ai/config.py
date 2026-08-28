from dataclasses import dataclass
import os
from pathlib import Path
from urllib.parse import urlsplit

import yaml

from .models import FeedConfig, Idea


@dataclass(frozen=True)
class Settings:
    api_key: str
    text_model: str
    image_model: str
    max_candidates: int = 20
    output_dir: Path = Path("automation/output")
    image_size: str = "1536x1024"
    image_quality: str = "medium"

    @classmethod
    def from_env(cls) -> "Settings":
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        return cls(
            api_key=api_key,
            text_model=os.environ.get("OPENAI_TEXT_MODEL", "gpt-5.6-terra"),
            image_model=os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2"),
        )


def _load_mapping(path: Path, key: str) -> list[dict]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict) or set(payload) != {key}:
        raise ValueError(f"expected only top-level key: {key}")
    values = payload[key]
    if not isinstance(values, list):
        raise ValueError(f"{key} must be a list")
    return values


def _require_https(value: object) -> None:
    if value is not None and urlsplit(str(value)).scheme.lower() != "https":
        raise ValueError("URLs must use HTTPS")


def load_ideas(path: Path) -> list[Idea]:
    values = _load_mapping(path, "ideas")
    for value in values:
        _require_https(value.get("url") if isinstance(value, dict) else None)
    return [Idea.model_validate(value) for value in values]


def load_feeds(path: Path) -> list[FeedConfig]:
    values = _load_mapping(path, "feeds")
    if not values:
        raise ValueError("feeds must not be empty")
    for value in values:
        _require_https(value.get("url") if isinstance(value, dict) else None)
    return [FeedConfig.model_validate(value) for value in values]
