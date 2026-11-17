"""Tests for batch generation from CSV and JSON files."""

import csv
import json

import pytest
from PIL import Image

from qrforge.batch import load_rows, run_batch


def _write_csv(path, rows):
    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_batch_csv_creates_one_file_per_row(tmp_path):
    source = tmp_path / "codes.csv"
    _write_csv(
        source,
        [
            {"data": "https://example.com", "output": "site.png"},
            {"data": "Hello batch", "output": "hello.png"},
            {"data": "https://python.org", "output": "python.png"},
        ],
    )
    written = run_batch(source, tmp_path / "out")
    assert len(written) == 3
    for path in written:
        assert path.exists() and path.stat().st_size > 0
        with Image.open(path) as image:
            assert image.format == "PNG"


def test_batch_json_creates_one_file_per_row(tmp_path):
    source = tmp_path / "codes.json"
    source.write_text(
        json.dumps(
            [
                {"data": "https://example.com"},
                {"data": "Second code"},
            ]
        ),
        encoding="utf-8",
    )
    written = run_batch(source, tmp_path / "out")
    assert len(written) == 2
    assert written[0].name == "qr-1.png"
    assert written[1].name == "qr-2.png"


def test_batch_wifi_row_builds_wifi_payload(tmp_path):
    source = tmp_path / "wifi.csv"
    _write_csv(
        source,
        [{"type": "wifi", "ssid": "HomeNet", "password": "secret", "output": "wifi.png"}],
    )
    written = run_batch(source, tmp_path / "out")
    assert len(written) == 1 and written[0].exists()


def test_batch_row_with_bad_type_names_the_row(tmp_path):
    source = tmp_path / "bad.csv"
    _write_csv(source, [{"data": "ok"}, {"type": "teleport", "data": "nope"}])
    with pytest.raises(ValueError, match="Row 2"):
        run_batch(source, tmp_path / "out")


def test_batch_missing_file_is_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        run_batch(tmp_path / "missing.csv", tmp_path / "out")


def test_batch_unsupported_suffix_is_rejected(tmp_path):
    source = tmp_path / "codes.txt"
    source.write_text("hello", encoding="utf-8")
    with pytest.raises(ValueError):
        load_rows(source)


def test_batch_empty_file_is_rejected(tmp_path):
    source = tmp_path / "empty.csv"
    source.write_text("data,output\n", encoding="utf-8")
    with pytest.raises(ValueError):
        run_batch(source, tmp_path / "out")
