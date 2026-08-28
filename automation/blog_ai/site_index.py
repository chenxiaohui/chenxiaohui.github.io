from pathlib import Path

import yaml


def _front_matter(path: Path) -> dict:
    total = 0
    lines: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        first = handle.readline()
        total += len(first.encode("utf-8"))
        if first.strip() != "---":
            raise ValueError(f"missing front matter: {path}")
        for line in handle:
            total += len(line.encode("utf-8"))
            if total > 65_536:
                raise ValueError(f"front matter exceeds 64 KiB: {path}")
            if line.strip().startswith("---") and set(line.strip()) == {"-"}:
                break
            lines.append(line)
        else:
            raise ValueError(f"unterminated front matter: {path}")
    return yaml.safe_load("".join(lines)) or {}


def load_public_title_index(posts_dir: Path, allowlist_path: Path) -> list[str]:
    allowlist = yaml.safe_load(allowlist_path.read_text(encoding="utf-8")) or {}
    reviewed = set(allowlist.get("tech", []))
    titles = []
    for path in sorted(posts_dir.glob("*")):
        if not path.is_file():
            continue
        data = _front_matter(path)
        relative_path = f"_posts/{path.name}"
        visible = relative_path in reviewed or (
            data.get("allow_ai_index") is True and data.get("channel") == "tech"
        )
        if visible and str(data.get("title", "")).strip():
            titles.append(str(data["title"]).strip())
    return titles
