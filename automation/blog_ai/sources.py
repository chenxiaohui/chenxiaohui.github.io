from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
import re
import socket
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

from .models import FeedConfig, Idea, SourceItem
from .network import fetch_url, normalized_url, validate_public_url


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _child_text(element: ET.Element, names: set[str]) -> str:
    for child in element:
        if _local_name(child.tag) in names:
            if child.text:
                return child.text
            return "".join(child.itertext())
    return ""


def _link(element: ET.Element, base_url: str) -> str:
    for child in element:
        if _local_name(child.tag) != "link":
            continue
        candidate = child.attrib.get("href") or child.text or ""
        if candidate and child.attrib.get("rel", "alternate") in {"alternate", ""}:
            return urljoin(base_url, candidate.strip())
    return ""


def _plain_text(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def _date(value: str) -> datetime | None:
    if not value.strip():
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def parse_feed(raw: bytes, base_url: str) -> list[SourceItem]:
    root = ET.fromstring(raw)
    entries = [element for element in root.iter() if _local_name(element.tag) in {"item", "entry"}]
    items = []
    for entry in entries:
        title = _plain_text(_child_text(entry, {"title"}))
        link = _link(entry, base_url)
        if not title or not link:
            continue
        published = _child_text(entry, {"pubDate", "published", "updated", "date"})
        summary = _child_text(entry, {"description", "summary", "content"})
        items.append(
            SourceItem(
                title=title,
                url=link,
                published_at=_date(published),
                excerpt=_plain_text(summary)[:2_000],
            )
        )
    return items


def fetch_sources(
    feeds: list[FeedConfig],
    ideas: list[Idea],
    opener=None,
    resolver=socket.getaddrinfo,
    max_candidates: int = 20,
) -> list[SourceItem]:
    allowed_hosts = {urlsplit(str(feed.url)).hostname for feed in feeds}
    allowed_hosts.update(urlsplit(str(idea.url)).hostname for idea in ideas if idea.url)
    allowed_hosts.discard(None)
    collected: list[SourceItem] = []

    for feed in feeds:
        body, final_url, _content_type = fetch_url(str(feed.url), allowed_hosts, resolver, opener, 2 * 1024 * 1024)
        for item in parse_feed(body, final_url):
            host = urlsplit(str(item.url)).hostname
            if not host:
                continue
            validate_public_url(str(item.url), {host}, resolver)
            allowed_hosts.add(host)
            collected.append(item)

    for idea in ideas:
        if not idea.url:
            continue
        host = urlsplit(str(idea.url)).hostname
        validate_public_url(str(idea.url), {host}, resolver)
        collected.append(SourceItem(title=idea.title, url=idea.url, published_at=None, excerpt=idea.note))

    unique = {normalized_url(str(item.url)): item for item in collected}
    ordered = sorted(
        unique.values(),
        key=lambda item: item.published_at.timestamp() if item.published_at else float("-inf"),
        reverse=True,
    )
    return ordered[:max_candidates]


class _ArticleTextParser(HTMLParser):
    SKIP = {"script", "style", "nav", "form"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.SKIP:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.SKIP and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data):
        if not self.skip_depth:
            self.parts.append(data)


def hydrate_sources(
    items: list[SourceItem],
    allowed_hosts: set[str],
    opener=None,
    resolver=socket.getaddrinfo,
) -> list[SourceItem]:
    hydrated = []
    for item in items:
        body, _final_url, content_type = fetch_url(
            str(item.url), allowed_hosts, resolver, opener, 1_572_864
        )
        if content_type != "text/html":
            raise ValueError("article response must use text/html")
        parser = _ArticleTextParser()
        parser.feed(body.decode("utf-8", errors="replace"))
        content = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()[:12_000]
        if len(content) < 400:
            raise ValueError("article text is too short")
        hydrated.append(item.model_copy(update={"content": content}))
    return hydrated
