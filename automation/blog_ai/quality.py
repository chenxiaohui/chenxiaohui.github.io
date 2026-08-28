from __future__ import annotations

import re
from urllib.parse import urlsplit

from .models import ArticleDraft, SourceItem
from .privacy import Finding, make_finding


def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+|[\u3400-\u9fff]", value.lower()))


def _normalized_title(value: str) -> str:
    return "".join(re.findall(r"[a-z0-9\u3400-\u9fff]+", value.lower()))


def _overlap(left: str, right: str) -> float:
    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / min(len(left_tokens), len(right_tokens))


class QualityGate:
    TIME_SENSITIVE = re.compile(r"\d|%|％|[$€£¥￥]|最新|目前|截至")

    def validate(
        self,
        draft: ArticleDraft,
        sources: list[SourceItem],
        titles: list[str],
    ) -> list[Finding]:
        findings: list[Finding] = []
        source_by_url = {str(source.url): source for source in sources}
        draft_urls = {str(url) for url in draft.source_urls}

        if draft.topic not in {"AI", "系统", "推荐", "工具"}:
            findings.append(make_finding("invalid_topic", "draft", 1, draft.topic))
        if not draft_urls or any(
            url not in source_by_url or urlsplit(url).scheme != "https" for url in draft_urls
        ):
            findings.append(make_finding("invalid_sources", "draft", 1, draft.title))

        time_sensitive = False
        for line_number, paragraph in enumerate(re.split(r"\n\s*\n", draft.body_markdown), start=1):
            if self.TIME_SENSITIVE.search(paragraph):
                time_sensitive = True
                if not any(url in paragraph for url in source_by_url):
                    findings.append(make_finding("uncited_time_sensitive", "body", line_number, paragraph))
        if time_sensitive and not draft.review_facts:
            findings.append(make_finding("missing_review_facts", "draft", 1, draft.title))

        chinese_characters = len(re.findall(r"[\u3400-\u9fff]", draft.body_markdown))
        if not 1_200 <= chinese_characters <= 2_500:
            findings.append(make_finding("invalid_body_length", "body", 1, draft.body_markdown))
        if len(re.findall(r"^##\s+", draft.body_markdown, re.MULTILINE)) < 3:
            findings.append(make_finding("missing_sections", "body", 1, draft.body_markdown))

        normalized = _normalized_title(draft.title)
        for title in titles:
            if normalized == _normalized_title(title) or _overlap(draft.title, title) > 0.8:
                findings.append(make_finding("duplicate_title", "title", 1, draft.title))
                break

        note_by_url = {str(note.url): note for note in draft.source_notes}
        if set(note_by_url) != draft_urls:
            findings.append(make_finding("incomplete_source_notes", "sources", 1, draft.title))
        for url, note in note_by_url.items():
            source = source_by_url.get(url)
            if source is None:
                continue
            for fact in note.facts:
                if _overlap(fact, source.content) < 0.5:
                    findings.append(make_finding("unsupported_source_fact", "source_note", 1, fact))
        if draft.source_conflicts:
            findings.append(make_finding("source_conflict", "sources", 1, draft.title))
        return findings
