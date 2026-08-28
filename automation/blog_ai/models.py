from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Idea(StrictModel):
    title: str
    url: HttpUrl | None = None
    note: str = ""


class FeedConfig(StrictModel):
    name: str
    url: HttpUrl


class SourceItem(StrictModel):
    title: str
    url: HttpUrl
    published_at: datetime | None
    excerpt: str
    content: str = ""


class TopicScore(StrictModel):
    source_urls: list[HttpUrl]
    title: str
    angle: str
    related_titles: list[str]
    topic: Literal["AI", "系统", "推荐", "工具"]
    relevance: int = Field(ge=0, le=5)
    source_quality: int = Field(ge=0, le=5)
    viewpoint_space: int = Field(ge=0, le=5)
    duplicate_risk: int = Field(ge=0, le=5)
    publish: bool
    rejection_reason: str = ""


class SourceNote(StrictModel):
    url: HttpUrl
    facts: list[str] = Field(min_length=1, max_length=5)


class ArticleDraft(StrictModel):
    title: str
    slug: str
    description: str
    topic: Literal["AI", "系统", "推荐", "工具"]
    body_markdown: str
    source_urls: list[HttpUrl]
    source_notes: list[SourceNote]
    source_conflicts: list[str]
    image_prompt: str
    image_alt: str
    review_facts: list[str]


class PipelineResult(StrictModel):
    status: Literal["generated", "no_candidate", "rejected"]
    post_path: Path | None = None
    image_path: Path | None = None
    packet_path: Path | None = None
    pr_body_path: Path | None = None
    reason: str = ""
