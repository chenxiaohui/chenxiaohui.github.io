from __future__ import annotations

from dataclasses import dataclass
import hashlib
import ipaddress
import re
from urllib.parse import urlsplit

from .network import normalized_url


@dataclass(frozen=True)
class Finding:
    code: str
    label: str
    line: int
    excerpt_hash: str


def make_finding(code: str, label: str, line: int, excerpt: str) -> Finding:
    digest = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()[:12]
    return Finding(code=code, label=label, line=line, excerpt_hash=digest)


class PrivacyGate:
    EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
    PHONE = re.compile(r"(?<!\w)\+?\d[\d ().-]{6,}\d(?!\w)")
    DATE_TIME = re.compile(r"\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?")
    URL = re.compile(r"https?://[^\s)<>'\"]+")
    SENSITIVE = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in [
            r"我在实际项目中",
            r"我们线上",
            r"内部(?:项目|代码|系统|实验|指标|文档)",
            r"业务指标",
            r"工作(?:截图|经历)",
            r"雇主",
            r"作为\s*AI",
            r"以下是",
            r"待补充",
            r"\b(?:our team|employer|internal (?:project|code|system|experiment)|business metrics?|work experience|screenshot|as an AI|TBD|TODO)\b",
        ]
    ]

    def __init__(self, allowed_source_urls: set[str]):
        self.allowed_source_urls = {normalized_url(url) for url in allowed_source_urls}

    def check_text(self, text: str, label: str) -> list[Finding]:
        findings: list[Finding] = []
        for line_number, line in enumerate(text.splitlines() or [text], start=1):
            if self.EMAIL.search(line):
                findings.append(make_finding("email", label, line_number, line))
            phone_text = self.DATE_TIME.sub("", line)
            for match in self.PHONE.finditer(phone_text):
                candidate = match.group()
                if sum(character.isdigit() for character in candidate) >= 10:
                    findings.append(make_finding("phone", label, line_number, line))
                    break
            for match in self.URL.finditer(line):
                candidate = match.group().rstrip(".,，。；;")
                try:
                    parsed = urlsplit(candidate)
                    host = parsed.hostname
                    if host:
                        try:
                            if not ipaddress.ip_address(host).is_global:
                                findings.append(make_finding("private_ip", label, line_number, line))
                                continue
                        except ValueError:
                            pass
                    if normalized_url(candidate) not in self.allowed_source_urls:
                        findings.append(make_finding("unapproved_url", label, line_number, line))
                except ValueError:
                    findings.append(make_finding("invalid_url", label, line_number, line))
            if any(pattern.search(line) for pattern in self.SENSITIVE):
                findings.append(make_finding("sensitive_claim", label, line_number, line))
            if "Harry Chen" in line and label != "disclosure":
                findings.append(make_finding("public_name_context", label, line_number, line))
        return findings
