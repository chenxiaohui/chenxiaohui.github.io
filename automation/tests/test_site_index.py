from pathlib import Path

from automation.blog_ai.site_index import load_public_title_index


def test_reads_only_opted_in_titles(tmp_path: Path):
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-01-01-private.md").write_text(
        "---\ntitle: Private legacy title\n---\nBODY_MUST_NOT_LEAK\n", encoding="utf-8"
    )
    (posts / "2026-01-02-public.md").write_text(
        "---\ntitle: Public title\nchannel: tech\nallow_ai_index: true\n---\nBODY_MUST_NOT_LEAK\n",
        encoding="utf-8",
    )
    allowlist = tmp_path / "allowlist.yml"
    allowlist.write_text("tech: []\nlife: []\n", encoding="utf-8")

    titles = load_public_title_index(posts, allowlist)

    assert titles == ["Public title"]
    assert all("BODY_MUST_NOT_LEAK" not in title for title in titles)


def test_includes_reviewed_legacy_tech_title(tmp_path: Path):
    posts = tmp_path / "_posts"
    posts.mkdir()
    path = posts / "2026-01-01-reviewed.md"
    path.write_text("---\ntitle: Reviewed title\n---\nprivate body\n", encoding="utf-8")
    allowlist = tmp_path / "allowlist.yml"
    allowlist.write_text("tech:\n  - _posts/2026-01-01-reviewed.md\nlife: []\n", encoding="utf-8")

    assert load_public_title_index(posts, allowlist) == ["Reviewed title"]
