"""Batch generation: make many QR codes at once from a CSV or JSON file.

Each row is one code. A row needs a ``data`` column (or, for the
special types, the columns that type needs) and may carry an
``output`` column for the file name. When no output name is given,
files are named ``qr-1.png``, ``qr-2.png`` and so on.

Row columns
-----------
``data``      text or URL to encode (for ``type=text``, the default)
``type``      ``text`` (default), ``wifi``, ``vcard``, ``email``,
              ``phone`` or ``sms``
``output``    file name inside the output directory
``fill_color``, ``back_color``, ``module_shape``, ``error_correction``,
``box_size``, ``border``, ``logo_path``   styling, as in the CLI

Type columns: ``wifi`` needs ``ssid``, ``password``, ``security``,
``hidden``; ``vcard`` needs ``name``, ``phone``, ``email``, ``org``;
``email`` needs ``address``, ``subject``, ``body``; ``phone`` and
``sms`` need ``number`` (and ``sms`` takes ``message``).
"""

import csv
import json
from pathlib import Path

from qrforge.generator import save_qr
from qrforge.models import QRConfig
from qrforge.payloads import (
    email_payload,
    phone_payload,
    sms_payload,
    vcard_payload,
    wifi_payload,
)


def _truthy(value) -> bool:
    return str(value).strip().lower() in ("true", "yes", "1")


def row_to_config(row: dict, index: int) -> tuple[QRConfig, str]:
    """Turn one batch row into a ``(QRConfig, output_name)`` pair.

    ``index`` is the 1-based row number, used in error messages and
    in the default file name.
    """
    kind = str(row.get("type") or "text").strip().lower()
    try:
        if kind == "wifi":
            data = wifi_payload(
                ssid=row.get("ssid", ""),
                password=row.get("password") or None,
                security=row.get("security") or "WPA",
                hidden=_truthy(row.get("hidden", "")),
            )
        elif kind == "vcard":
            data = vcard_payload(
                name=row.get("name", ""),
                phone=row.get("phone") or None,
                email=row.get("email") or None,
                org=row.get("org") or None,
            )
        elif kind == "email":
            data = email_payload(
                row.get("address", ""),
                subject=row.get("subject") or None,
                body=row.get("body") or None,
            )
        elif kind == "phone":
            data = phone_payload(row.get("number", ""))
        elif kind == "sms":
            data = sms_payload(
                row.get("number", ""), message=row.get("message") or None
            )
        elif kind == "text":
            data = (row.get("data") or "").strip()
            if not data:
                raise ValueError("a text row needs a 'data' value")
        else:
            raise ValueError(f"unknown type {kind!r}")
    except ValueError as exc:
        raise ValueError(f"Row {index}: {exc}") from None

    output = (row.get("output") or "").strip() or f"qr-{index}.png"
    config = QRConfig(
        data,
        error_correction=(row.get("error_correction") or "M").strip().upper(),
        box_size=int(row.get("box_size") or 10),
        border=int(row.get("border") or 4),
        fill_color=(row.get("fill_color") or "black").strip(),
        back_color=(row.get("back_color") or "white").strip(),
        module_shape=(row.get("module_shape") or "square").strip(),
        logo_path=(row.get("logo_path") or None),
    )
    return config, output


def load_rows(input_path: str | Path) -> list[dict]:
    """Read batch rows from a ``.csv`` or ``.json`` file."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Batch file not found: {path}")
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    if path.suffix.lower() == ".json":
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list) or not all(
            isinstance(row, dict) for row in rows
        ):
            raise ValueError("A JSON batch file must hold a list of objects.")
        return rows
    raise ValueError(f"Unsupported batch file type: {path.suffix!r} (use .csv or .json).")


def run_batch(input_path: str | Path, output_dir: str | Path) -> list[Path]:
    """Generate one QR code per row and return the files written.

    Raises ``ValueError`` naming the row when a row is invalid, so
    a bad row is easy to find in a long file.
    """
    rows = load_rows(input_path)
    if not rows:
        raise ValueError(f"No rows found in {input_path}.")
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for index, row in enumerate(rows, start=1):
        config, output = row_to_config(row, index)
        written.append(save_qr(config, out_dir / output))
    return written
