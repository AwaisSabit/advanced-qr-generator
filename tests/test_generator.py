"""Tests for core QR generation: text, URLs and error correction."""

import pytest
from PIL import Image

from qrforge.generator import (
    describe_qr,
    generate_image,
    qr_matrix,
    render_terminal,
    save_qr,
)
from qrforge.models import QRConfig


def test_text_qr_produces_valid_image(tmp_path):
    path = save_qr(QRConfig("Hello, QRForge!"), tmp_path / "hello.png")
    assert path.exists() and path.stat().st_size > 0
    with Image.open(path) as image:
        assert image.format == "PNG"
        assert image.size[0] == image.size[1]  # QR codes are square
        assert image.size[0] > 0


def test_url_qr_image_is_not_blank():
    image = generate_image(QRConfig("https://example.com"))
    pixels = list(image.getdata())
    assert any(p != (255, 255, 255) for p in pixels)  # dark modules exist
    assert any(p == (255, 255, 255) for p in pixels)  # light modules exist


@pytest.mark.parametrize("level", ["L", "M", "Q", "H"])
def test_all_error_correction_levels_work(level):
    image = generate_image(QRConfig("https://example.com", error_correction=level))
    assert image.size[0] > 0
    info = describe_qr(QRConfig("https://example.com", error_correction=level))
    assert info["error_correction"] == level
    assert info["version"] >= 1


def test_empty_data_is_rejected():
    with pytest.raises(ValueError):
        QRConfig("")


def test_bad_error_correction_is_rejected():
    with pytest.raises(ValueError):
        QRConfig("hello", error_correction="X")


def test_matrix_is_square_and_matches_image_size():
    config = QRConfig("https://example.com", box_size=10, border=4)
    matrix = qr_matrix(config)
    assert len(matrix) == len(matrix[0])
    image = generate_image(config)
    assert image.size[0] == len(matrix) * config.box_size


def test_terminal_output_draws_blocks():
    text = render_terminal(QRConfig("hi"))
    assert "██" in text
    assert len(text.splitlines()) > 10


def test_describe_reports_version_and_modules():
    info = describe_qr(QRConfig("https://example.com"))
    assert info["data"] == "https://example.com"
    assert info["data_length"] == len("https://example.com")
    assert info["modules"] > 20
    assert info["image_size_px"] == info["modules"] * info["box_size"]
