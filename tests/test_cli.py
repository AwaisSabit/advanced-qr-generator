"""Tests for the command line interface: every subcommand."""

import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest
from PIL import Image

from qrforge.cli import main


def test_cli_generate_exits_zero_and_writes_png(tmp_path):
    out = tmp_path / "site.png"
    assert main(["generate", "https://example.com", "--output", str(out)]) == 0
    assert out.exists() and out.stat().st_size > 0
    with Image.open(out) as image:
        assert image.format == "PNG"


def test_cli_generate_without_output_draws_in_terminal(capsys):
    assert main(["generate", "hello"]) == 0
    assert "██" in capsys.readouterr().out


def test_cli_wifi_exits_zero_and_writes_svg(tmp_path):
    out = tmp_path / "wifi.svg"
    assert main([
        "wifi", "--ssid", "MyHomeWiFi", "--password", "secret123",
        "--output", str(out),
    ]) == 0
    root = ET.parse(out).getroot()
    assert root.tag.endswith("svg")


def test_cli_wifi_open_network(tmp_path):
    out = tmp_path / "open.png"
    assert main([
        "wifi", "--ssid", "CoffeeShop", "--security", "nopass",
        "--output", str(out),
    ]) == 0
    assert out.exists()


def test_cli_wifi_without_password_fails(tmp_path):
    assert main([
        "wifi", "--ssid", "Home", "--output", str(tmp_path / "x.png"),
    ]) == 2


def test_cli_vcard_exits_zero(tmp_path):
    out = tmp_path / "contact.png"
    assert main([
        "vcard", "--name", "Awais Sabit", "--phone", "+92 300 1234567",
        "--email", "awaissabit@gmail.com", "--output", str(out),
    ]) == 0
    assert out.exists() and out.stat().st_size > 0


def test_cli_email_phone_sms_exit_zero(tmp_path):
    assert main(["email", "awaissabit@gmail.com", "--output",
                 str(tmp_path / "mail.png")]) == 0
    assert main(["phone", "+92 300 1234567", "--output",
                 str(tmp_path / "phone.png")]) == 0
    assert main(["sms", "+92 300 1234567", "--message", "Hello!",
                 "--output", str(tmp_path / "sms.png")]) == 0


def test_cli_batch_exits_zero(tmp_path):
    source = tmp_path / "codes.csv"
    source.write_text("data,output\nhttps://example.com,site.png\nHello,hi.png\n",
                      encoding="utf-8")
    assert main(["batch", str(source), "--output-dir", str(tmp_path / "out")]) == 0
    assert (tmp_path / "out" / "site.png").exists()
    assert (tmp_path / "out" / "hi.png").exists()


def test_cli_info_reports_facts(capsys):
    assert main(["info", "https://example.com"]) == 0
    out = capsys.readouterr().out
    assert "QR version:" in out
    assert "Error correction: M" in out
    assert "Modules:" in out


def test_cli_version_and_help():
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_cli_generate_with_style_options(tmp_path):
    out = tmp_path / "styled.png"
    assert main([
        "generate", "https://example.com", "--output", str(out),
        "--shape", "dots", "--fill", "#1a5276", "--error-correction", "H",
    ]) == 0
    with Image.open(out) as image:
        assert b"\x1a\x52\x76" in image.tobytes()  # #1a5276 modules present


def test_cli_as_module_exits_zero(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "qrforge", "generate", "hello",
         "--output", str(tmp_path / "m.png")],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "m.png").exists()
