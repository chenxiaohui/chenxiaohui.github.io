from __future__ import annotations

from dataclasses import dataclass
import hashlib
from io import BytesIO
import os
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError


@dataclass(frozen=True)
class ImageInfo:
    path: Path
    width: int
    height: int
    size_bytes: int
    sha256: str


def save_cover(raw: bytes, target: Path, max_bytes: int = 450 * 1024) -> ImageInfo:
    try:
        with Image.open(BytesIO(raw)) as source:
            fitted = ImageOps.fit(
                source.convert("RGB"),
                (1536, 1024),
                method=Image.Resampling.LANCZOS,
            )
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("generated cover is not a valid image") from exc

    encoded = None
    for quality in (82, 78, 74, 70):
        buffer = BytesIO()
        fitted.save(buffer, format="WEBP", quality=quality, method=6)
        candidate = buffer.getvalue()
        if len(candidate) <= max_bytes:
            encoded = candidate
            break
    if encoded is None:
        raise ValueError("generated cover cannot meet the 450 KiB limit")

    with Image.open(BytesIO(encoded)) as verified:
        if verified.format != "WEBP" or verified.size != (1536, 1024) or verified.mode != "RGB":
            raise ValueError("generated cover failed format validation")
        if verified.getexif() or {"exif", "icc_profile", "xmp"} & set(verified.info):
            raise ValueError("generated cover still contains metadata")

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.tmp")
    temporary.write_bytes(encoded)
    os.replace(temporary, target)
    return ImageInfo(
        path=target,
        width=1536,
        height=1024,
        size_bytes=len(encoded),
        sha256=hashlib.sha256(encoded).hexdigest(),
    )
