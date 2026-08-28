from __future__ import annotations

import ipaddress
import socket
from typing import Callable
from urllib.error import HTTPError
from urllib.parse import SplitResult, urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _normalized_host(host: str) -> str:
    return host.rstrip(".").encode("idna").decode("ascii").lower()


def _addresses(host: str, resolver: Callable) -> list[str]:
    records = resolver(host, 443, type=socket.SOCK_STREAM)
    addresses = []
    for record in records:
        if isinstance(record, str):
            addresses.append(record)
        else:
            addresses.append(record[4][0])
    return list(dict.fromkeys(addresses))


def validate_public_url(url: str, allowed_hosts: set[str], resolver: Callable = socket.getaddrinfo) -> SplitResult:
    parsed = urlsplit(url)
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("invalid URL port") from exc
    if parsed.scheme.lower() != "https":
        raise ValueError("URL must use HTTPS")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URL credentials are not allowed")
    if port not in (None, 443):
        raise ValueError("URL port must be 443")
    if not parsed.hostname:
        raise ValueError("URL hostname is required")

    host = _normalized_host(parsed.hostname)
    normalized_allowlist = {_normalized_host(value) for value in allowed_hosts}
    if host not in normalized_allowlist:
        raise ValueError("hostname is outside the allowlist")

    addresses = _addresses(host, resolver)
    if not addresses:
        raise ValueError("hostname did not resolve")
    for address in addresses:
        try:
            public = ipaddress.ip_address(address).is_global
        except ValueError as exc:
            raise ValueError("resolver returned an invalid address") from exc
        if not public:
            raise ValueError("hostname resolved to a non-public address")

    netloc = host if port is None else f"{host}:{port}"
    return SplitResult("https", netloc, parsed.path or "/", parsed.query, parsed.fragment)


def normalized_url(url: str) -> str:
    parsed = urlsplit(url)
    host = _normalized_host(parsed.hostname or "")
    netloc = host if parsed.port in (None, 443) else f"{host}:{parsed.port}"
    return urlunsplit((parsed.scheme.lower(), netloc, parsed.path or "/", parsed.query, ""))


def _default_open(request: Request, timeout: int = 15):
    return build_opener(_NoRedirect()).open(request, timeout=timeout)


def _open(opener, request: Request):
    try:
        if hasattr(opener, "open"):
            return opener.open(request, timeout=15)
        return opener(request, timeout=15)
    except HTTPError as error:
        if error.code in {301, 302, 303, 307, 308}:
            return error
        raise


def fetch_url(
    url: str,
    allowed_hosts: set[str],
    resolver: Callable = socket.getaddrinfo,
    opener=None,
    max_bytes: int = 2 * 1024 * 1024,
) -> tuple[bytes, str, str]:
    opener = opener or _default_open
    current = normalized_url(url)
    for redirect_count in range(4):
        validate_public_url(current, allowed_hosts, resolver)
        request = Request(current, headers={"User-Agent": "HarryChenBlogDraft/1.0", "Accept": "*/*"})
        response = _open(opener, request)
        try:
            status = getattr(response, "status", getattr(response, "code", None))
            if status in {301, 302, 303, 307, 308}:
                if redirect_count == 3:
                    raise ValueError("too many redirects")
                location = response.headers.get("Location")
                if not location:
                    raise ValueError("redirect is missing Location")
                current = normalized_url(urljoin(current, location))
                validate_public_url(current, allowed_hosts, resolver)
                continue
            if status != 200:
                raise ValueError(f"unexpected HTTP status: {status}")
            body = response.read(max_bytes + 1)
            if len(body) > max_bytes:
                raise ValueError("response body is too large")
            headers = response.headers
            content_type = headers.get_content_type() if hasattr(headers, "get_content_type") else headers.get("Content-Type", "").split(";", 1)[0]
            return body, current, content_type.lower()
        finally:
            response.close()
    raise ValueError("redirect limit exceeded")
