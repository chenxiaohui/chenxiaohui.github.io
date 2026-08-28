import socket
from urllib.parse import urlsplit

import pytest

from automation.blog_ai.network import validate_public_url


def public_resolver(host, port, type=socket.SOCK_STREAM):
    return [(socket.AF_INET, type, 6, "", ("93.184.216.34", port))]


def fake_resolver(host, port, type=socket.SOCK_STREAM):
    addresses = {
        "localhost": "127.0.0.1",
        "127.0.0.1": "127.0.0.1",
        "169.254.169.254": "169.254.169.254",
        "10.0.0.2": "10.0.0.2",
        "::1": "::1",
    }
    address = addresses[host]
    family = socket.AF_INET6 if ":" in address else socket.AF_INET
    target = (address, port, 0, 0) if family == socket.AF_INET6 else (address, port)
    return [(family, type, 6, "", target)]


@pytest.mark.parametrize(
    "url",
    [
        "https://localhost/feed",
        "https://127.0.0.1/feed",
        "https://169.254.169.254/feed",
        "https://10.0.0.2/feed",
        "https://[::1]/feed",
    ],
)
def test_rejects_non_public_hosts(url):
    host = urlsplit(url).hostname
    with pytest.raises(ValueError):
        validate_public_url(url, {host}, fake_resolver)


def test_rejects_host_outside_allowlist():
    with pytest.raises(ValueError, match="allowlist"):
        validate_public_url("https://other.example/feed", {"example.com"}, public_resolver)


@pytest.mark.parametrize(
    "url",
    ["http://example.com/feed", "https://user@example.com/feed", "https://example.com:444/feed"],
)
def test_rejects_unsafe_url_shapes(url):
    with pytest.raises(ValueError):
        validate_public_url(url, {"example.com"}, public_resolver)
