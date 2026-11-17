"""Tests for output formats: SVG and terminal output alongside PNG."""

import xml.etree.ElementTree as ET

from qrforge.generator import generate_svg_text, render_terminal, save_qr
from qrforge.models import QRConfig


def test_svg_output_is_valid_xml(tmp_path):
    path = save_qr(QRConfig("https://example.com"), tmp_path / "code.svg")
    assert path.exists() and path.stat().st_size > 0
    root = ET.parse(path).getroot()
    assert root.tag.endswith("svg")
    assert len(list(root)) > 0  # the code path is present


def test_svg_text_contains_svg_root_and_path():
    text = generate_svg_text(QRConfig("Hello, QRForge!"))
    assert text.startswith("<?xml")
    assert "<svg" in text
    assert "<path" in text


def test_svg_and_png_hold_the_same_data():
    config = QRConfig("https://example.com")
    svg = generate_svg_text(config)
    assert "M4,4" in svg  # the finder pattern starts at module (4, 4)
    png_text = render_terminal(config)
    assert "██" in png_text


def test_save_qr_defaults_to_png_without_suffix(tmp_path):
    path = save_qr(QRConfig("hello"), tmp_path / "code")
    assert path.suffix == ".png"
    assert path.exists()


def test_terminal_output_is_square_text():
    text = render_terminal(QRConfig("https://example.com"))
    lines = text.splitlines()
    assert len(lines) > 20
    assert all(len(line) == len(lines[0]) for line in lines)
    assert all(set(line) <= {"█", " "} for line in lines)
