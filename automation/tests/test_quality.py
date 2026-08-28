from automation.blog_ai.models import ArticleDraft, SourceItem, SourceNote
from automation.blog_ai.quality import QualityGate


SOURCE_URL = "https://example.com/source"


def source():
    return SourceItem(
        title="Public source",
        url=SOURCE_URL,
        published_at=None,
        excerpt="Documented mechanism",
        content="Documented public mechanism explains system tradeoff and design constraints in detail.",
    )


def draft(**updates):
    body = "\n\n".join(
        [
            "## 机制",
            "公开系统机制与设计取舍。" * 50,
            "## 边界",
            "公开资料说明系统边界与约束。" * 50,
            "## 开放问题",
            "仍需根据公开文档核对机制与限制。" * 50,
        ]
    )
    values = dict(
        title="Public systems article",
        slug="public-systems-article",
        description="A concise public-source description",
        topic="系统",
        body_markdown=body,
        source_urls=[SOURCE_URL],
        source_notes=[SourceNote(url=SOURCE_URL, facts=["Documented public mechanism explains system tradeoff"])],
        source_conflicts=[],
        image_prompt="abstract systems illustration",
        image_alt="抽象的软件系统节点与数据流插画",
        review_facts=[],
    )
    values.update(updates)
    return ArticleDraft(**values)


def test_accepts_evidenced_non_repetitive_draft():
    assert QualityGate().validate(draft(), [source()], ["Different article"]) == []


def test_rejects_numeric_paragraph_without_source_link():
    value = draft(body_markdown=draft().body_markdown + "\n\n目前性能提升 20%。")
    codes = {finding.code for finding in QualityGate().validate(value, [source()], [])}
    assert "uncited_time_sensitive" in codes
    assert "missing_review_facts" in codes


def test_allows_time_sensitive_paragraph_with_source_and_review_fact():
    body = draft().body_markdown + f"\n\n截至 2026 年，公开文档给出该约束。[来源]({SOURCE_URL})"
    value = draft(body_markdown=body, review_facts=["核对公开文档日期"])
    assert QualityGate().validate(value, [source()], []) == []


def test_rejects_duplicate_title():
    codes = {finding.code for finding in QualityGate().validate(draft(), [source()], ["Public systems article"])}
    assert "duplicate_title" in codes


def test_rejects_high_title_overlap():
    codes = {
        finding.code
        for finding in QualityGate().validate(draft(), [source()], ["Public systems article explained"])
    }
    assert "duplicate_title" in codes


def test_rejects_uncovered_or_unsupported_source_note():
    value = draft(source_notes=[SourceNote(url=SOURCE_URL, facts=["unrelated pineapple statement"])])
    codes = {finding.code for finding in QualityGate().validate(value, [source()], [])}
    assert "unsupported_source_fact" in codes
