"""Tests for logo embedding in the centre of a QR code."""

from pathlib import Path

import pytest
from PIL import Image

from qrforge.generator import generate_image
from qrforge.logo import embed_logo
from qrforge.models import QRConfig


def _make_logo(path: Path, color=(220, 30, 30), size=100) -> Path:
    logo = Image.new("RGB", (size, size), color)
    logo.save(path)
    return path


def test_logo_embedding_keeps_size_and_adds_logo_pixels(tmp_path):
    logo = _make_logo(tmp_path / "logo.png")
    plain = generate_image(QRConfig("https://example.com", error_correction="H"))
    with_logo = generate_image(
        QRConfig("https://example.com", error_correction="H", logo_path=str(logo))
    )
    assert with_logo.size == plain.size
    assert with_logo.tobytes() != plain.tobytes()
    # The centre of the code now carries the red logo.
    cx, cy = with_logo.width // 2, with_logo.height // 2
    centre = with_logo.crop((cx - 10, cy - 10, cx + 10, cy + 10))
    assert (220, 30, 30) in set(centre.getdata())


def test_logo_embedding_works_with_styled_code(tmp_path):
    logo = _make_logo(tmp_path / "logo.png")
    image = generate_image(
        QRConfig(
            "https://example.com",
            error_correction="H",
            module_shape="rounded",
            logo_path=str(logo),
        )
    )
    assert image.size[0] > 0


def test_missing_logo_file_is_rejected(tmp_path):
    image = generate_image(QRConfig("https://example.com"))
    with pytest.raises(FileNotFoundError):
        embed_logo(image, tmp_path / "no-such-logo.png")


def test_logo_scale_out_of_range_is_rejected():
    with pytest.raises(ValueError):
        QRConfig("hello", logo_scale=0.5)
