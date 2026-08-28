from pathlib import Path
import socket

import pytest

from automation.blog_ai.models import SourceItem
from automation.blog_ai.sources import hydrate_sources, parse_feed


FIXTURE = Path(__file__).parent / "fixtures" / "feed.xml"


def public_resolver(host, port, type=socket.SOCK_STREAM):
    return [(socket.AF_INET, type, 6, "", ("93.184.216.34", port))]


class Headers(dict):
    def get_content_type(self):
        return self.get("Content-Type", "").split(";", 1)[0]


class Response:
    def __init__(self, body=b"", status=200, content_type="text/html", location=None, url="https://example.com/article"):
        self.body = body
        self.status = status
        self.headers = Headers({"Content-Type": content_type})
        if location:
            self.headers["Location"] = location
        self.url = url

    def read(self, amount=-1):
        return self.body if amount < 0 else self.body[:amount]

    def geturl(self):
        return self.url

    def close(self):
        pass


class SequenceOpener:
    def __init__(self, responses):
        self.responses = iter(responses)

    def __call__(self, request, timeout=15):
        return next(self.responses)


def item(url="https://example.com/article"):
    return SourceItem(title="Article", url=url, published_at=None, excerpt="Public excerpt")


def test_parses_rss_fixture():
    items = parse_feed(FIXTURE.read_bytes(), base_url="https://example.com/feed.xml")
    assert items[0].title == "Public release"
    assert str(items[0].url) == "https://example.com/posts/release"
    assert items[0].published_at is not None
    assert items[1].published_at is None


def test_hydrates_valid_html_article():
    body = ("<html><nav>skip</nav><main><p>" + "公开系统说明。" * 80 + "</p></main><script>skip</script></html>").encode()
    result = hydrate_sources([item()], {"example.com"}, SequenceOpener([Response(body)]), public_resolver)
    assert len(result[0].content) >= 400
    assert "skip" not in result[0].content


def test_rejects_redirect_to_non_allowlisted_host():
    opener = SequenceOpener([Response(status=302, location="https://other.example/article")])
    with pytest.raises(ValueError, match="allowlist"):
        hydrate_sources([item()], {"example.com"}, opener, public_resolver)


def test_rejects_non_html_content():
    opener = SequenceOpener([Response(b"binary", content_type="application/octet-stream")])
    with pytest.raises(ValueError, match="text/html"):
        hydrate_sources([item()], {"example.com"}, opener, public_resolver)


def test_rejects_oversized_article():
    opener = SequenceOpener([Response(b"x" * (1_572_864 + 1))])
    with pytest.raises(ValueError, match="large"):
        hydrate_sources([item()], {"example.com"}, opener, public_resolver)


def test_rejects_too_short_article():
    opener = SequenceOpener([Response(b"<html><main>short</main></html>")])
    with pytest.raises(ValueError, match="short"):
        hydrate_sources([item()], {"example.com"}, opener, public_resolver)
