from pathlib import Path

import pytest

from automation.blog_ai.config import Settings, load_feeds


def test_settings_defaults(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    settings = Settings.from_env()
    assert settings.text_model == "gpt-5.6-terra"
    assert settings.image_model == "gpt-image-2"
    assert settings.max_candidates == 20


def test_feed_must_use_https(tmp_path: Path):
    path = tmp_path / "feeds.yml"
    path.write_text("feeds:\n  - name: bad\n    url: http://example.com/feed.xml\n", encoding="utf-8")
    with pytest.raises(ValueError, match="HTTPS"):
        load_feeds(path)
