import base64
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace

from PIL import Image
import pytest

from automation.blog_ai.image import save_cover
from automation.blog_ai.openai_client import OpenAIWriter


FIXTURE = Path(__file__).parent / "fixtures" / "source.png"


class FakeImages:
    def __init__(self, raw):
        self.raw = raw
        self.calls = []

    def generate(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(data=[SimpleNamespace(b64_json=base64.b64encode(self.raw).decode("ascii"))])


class FakeClient:
    def __init__(self, raw):
        self.images = FakeImages(raw)


def test_image_api_uses_fixed_model_size_and_quality(tmp_path: Path):
    (tmp_path / "image_generation.md").write_text("No text or logos.", encoding="utf-8")
    client = FakeClient(FIXTURE.read_bytes())
    writer = OpenAIWriter(client, "gpt-5.6-terra", tmp_path, image_model="gpt-image-2")

    raw = writer.generate_image("abstract public system")

    assert raw == FIXTURE.read_bytes()
    assert client.images.calls == [
        {
            "model": "gpt-image-2",
            "prompt": "No text or logos.\n\nabstract public system",
            "size": "1536x1024",
            "quality": "medium",
        }
    ]


def test_save_cover_removes_metadata_and_caps_size(tmp_path: Path):
    target = tmp_path / "cover.webp"

    info = save_cover(FIXTURE.read_bytes(), target)

    assert info.path == target
    assert info.width == 1536
    assert info.height == 1024
    assert info.size_bytes <= 450 * 1024
    with Image.open(target) as image:
        assert image.format == "WEBP"
        assert image.mode == "RGB"
        assert image.size == (1536, 1024)
        assert not image.getexif()
        assert not ({"exif", "icc_profile", "xmp", "author"} & set(image.info))


def test_save_cover_raises_when_limit_cannot_be_met(tmp_path: Path):
    with pytest.raises(ValueError, match="450 KiB"):
        save_cover(FIXTURE.read_bytes(), tmp_path / "cover.webp", max_bytes=1)
