import pytest

from automation.blog_ai.privacy import PrivacyGate


@pytest.mark.parametrize(
    "text",
    [
        "contact me at person@example.com",
        "call 415-555-1212",
        "see https://10.0.0.1/private",
        "see https://[::1]/private",
        "see https://other.example/source",
        "我在实际项目中使用过这个方案",
        "我们线上采用了内部代码",
        "内部实验显示业务指标增长",
        "这里附上工作截图和工作经历",
        "作为 AI，以下是待补充内容",
    ],
)
def test_rejects_sensitive_text(text):
    findings = PrivacyGate({"https://example.com/source"}).check_text(text, "body")
    assert findings
    assert all(len(finding.excerpt_hash) == 12 for finding in findings)


def test_allows_generic_public_technical_discussion():
    text = "公开资料讨论 AI、软件系统、推荐方法和开源工具。来源：https://example.com/source"
    assert PrivacyGate({"https://example.com/source"}).check_text(text, "body") == []


def test_public_name_is_limited_to_disclosure_metadata():
    gate = PrivacyGate(set())
    assert gate.check_text("由 AI 协助整理，经 Harry Chen 审核", "disclosure") == []
    assert gate.check_text("Harry Chen 使用了这个工具", "body")
