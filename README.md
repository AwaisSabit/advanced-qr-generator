# QRForge — Advanced QR Code Generator

Generate QR codes in Python for text, URLs, WiFi networks, contacts
(vCard), email, phone numbers and SMS — with colours, module shapes,
a logo in the centre, PNG, SVG and terminal output, and batch
generation from CSV or JSON files.

> Built as part of a 30-day portfolio challenge, Nov–Dec 2026.

## Problem

Most QR tools only make a plain black-and-white code for a link.
Sharing WiFi, a contact card or a branded code needs the right
payload format, error correction and styling — QRForge puts all of
that in one small, tested command line tool and Python library.

## Features

- Text and URL QR codes with four error correction levels (L, M, Q, H)
- Styled codes: custom colours, rounded, square, dot and gapped modules
- WiFi QR codes (WPA, WEP, open networks, hidden SSID)
- vCard contact QR codes
- Email, phone and SMS QR codes
- Logo embedded in the centre of a code
- PNG, SVG and terminal output
- Batch generation from CSV and JSON files
- Command line interface with `generate`, `wifi`, `vcard`, `batch`
  and `info` subcommands

## Stack

- Python 3.11+
- [qrcode](https://github.com/lincolnloop/python-qrcode) (`qrcode[pil]`)
  for all QR encoding
- [Pillow](https://python-pillow.org/) for image rendering and logos
- pytest for tests

## Install

Requires Python 3.11 or newer.

```bash
git clone https://github.com/AwaisSabit/advanced-qr-generator.git
cd advanced-qr-generator
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .[test]           # editable install, including pytest
```

## Usage

```bash
qrforge generate "https://example.com" --output hello.png
qrforge wifi --ssid "MyHomeWiFi" --password "secret123" --output wifi.png
qrforge vcard --name "Awais Sabit" --phone "+92 300 1234567" --output contact.png
qrforge batch codes.csv --output-dir generated
qrforge info "https://example.com"
python -m qrforge --help
```

See the full usage guide, examples and limitations below as the
project grows — the final documentation is added with version 1.0.0.

## Tests

```bash
python -m pytest -q
```

## Limitations

- QR codes have a maximum data capacity that depends on the error
  correction level; very long text with level H may fail to fit.
- A logo in the centre covers part of the code, so use error
  correction level H (or at least Q) with a logo.
- SVG output is a single-colour vector code; styled module shapes
  are a PNG feature.

## License

MIT — see [LICENSE](LICENSE).
