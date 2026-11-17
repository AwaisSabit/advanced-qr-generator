"""Tests for styled QR codes: colours and module shapes."""

import pytest

from qrforge.generator import generate_image
from qrforge.models import QRConfig
from qrforge.styles import validate_color


@pytest.mark.parametrize(
    "shape", ["square", "rounded", "dots", "gapped", "bars", "bars-horizontal"]
)
def test_each_module_shape_renders(shape):
    image = generate_image(QRConfig("https://example.com", module_shape=shape))
    assert image.size[0] > 0


def test_styled_output_differs_by_shape():
    plain = generate_image(QRConfig("https://example.com", module_shape="square"))
    dots = generate_image(QRConfig("https://example.com", module_shape="dots"))
    assert plain.tobytes() != dots.tobytes()


def test_styled_output_differs_by_colour():
    black = generate_image(QRConfig("https://example.com", fill_color="black"))
    navy = generate_image(QRConfig("https://example.com", fill_color="#000080"))
    assert black.tobytes() != navy.tobytes()
    assert (0, 0, 128) in set(navy.getdata())


def test_invalid_colour_is_rejected():
    with pytest.raises(ValueError):
        validate_color("not-a-colour")


def test_invalid_shape_is_rejected():
    with pytest.raises(ValueError):
        QRConfig("hello", module_shape="triangle")
