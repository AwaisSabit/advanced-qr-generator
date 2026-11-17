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
- Styled codes: custom colours, rounded, square, dot, gapped and bar modules
- WiFi QR codes (WPA, WEP, open networks, hidden SSID)
- vCard contact QR codes
- Email, phone and SMS QR codes
- Logo embedded in the centre of a code (use error correction H)
- PNG, SVG and terminal output
- Batch generation from CSV and JSON files
- Command line interface with `generate`, `wifi`, `vcard`, `email`,
  `phone`, `sms`, `batch` and `info` subcommands

## Stack

- Python 3.11+
- [qrcode](https://github.com/lincolnloop/python-qrcode) (`qrcode[pil]`)
  for all QR encoding (version 8.2)
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

### Text and URLs

```bash
qrforge generate "https://example.com" --output website.png
qrforge generate "Hello, world!" --output hello.svg   # vector output
qrforge generate "https://example.com"                # draws in the terminal
```

### WiFi

```bash
qrforge wifi --ssid "MyHomeWiFi" --password "secret123" --output wifi.png
qrforge wifi --ssid "CoffeeShop" --security nopass --output open.png
qrforge wifi --ssid "HiddenNet" --password "secret123" --hidden --output hidden.png
```

A phone that scans the code offers to join the network. The payload
follows the standard format, for example
`WIFI:T:WPA;S:MyHomeWiFi;P:secret123;;`.

### Contacts (vCard)

```bash
qrforge vcard --name "Awais Sabit" --phone "+92 300 1234567" \
    --email "awaissabit@gmail.com" --org "Mugazi Kitchen" \
    --output contact.png
```

A phone that scans the code offers to save the contact.

### Email, phone and SMS

```bash
qrforge email awaissabit@gmail.com --subject "Hello" --body "How are you?" --output mail.png
qrforge phone "+92 300 1234567" --output call.png
qrforge sms "+92 300 1234567" --message "Hello!" --output text.png
```

### Styling and logos

```bash
qrforge generate "https://github.com/AwaisSabit" --output styled.png \
    --shape dots --fill "#1a5276" --error-correction H --logo logo.png
```

Module shapes: `square`, `rounded`, `dots`, `gapped`, `bars`,
`bars-horizontal`. Colours are names (`navy`) or hex (`#1a5276`).
Error correction: `L` (7% recovery), `M` (15%), `Q` (25%),
`H` (30%). Use `H` (or at least `Q`) with a logo, since the logo
covers the centre modules.

### Batch generation

One code per row, from a CSV or JSON file:

```bash
qrforge batch examples/sample.csv --output-dir generated
```

`examples/sample.csv` shows the columns: `data`, `type`, `output`,
`fill_color`, `module_shape`. Rows can also be `type=wifi` (with
`ssid`, `password`, `security`, `hidden`), `type=vcard` (with
`name`, `phone`, `email`, `org`), `type=email`, `type=phone` or
`type=sms`. A JSON file holds a list of the same row objects.
Rows without an `output` name are saved as `qr-1.png`, `qr-2.png`
and so on, and a bad row fails with its row number in the message.

### Inspect a code

```bash
qrforge info "https://example.com"
```

```text
Data: https://example.com
Data length: 19 characters
QR version: 2
Error correction: M (15% recovery)
Modules: 33 x 33
Image size: 330 x 330 px
```

### As a library

```python
from qrforge import QRConfig, save_qr
from qrforge.payloads import wifi_payload

config = QRConfig(
    wifi_payload("MyHomeWiFi", "secret123"),
    error_correction="H",
    module_shape="rounded",
    fill_color="#1a5276",
)
save_qr(config, "wifi.png")   # PNG; use a .svg path for vector output
```

### Demo

```bash
python examples/demo.py        # writes examples/output/*.png and *.svg
```

## Tests

```bash
python -m pytest -q
```

69 tests cover core generation, error correction levels, styling,
WiFi/vCard/email/phone/SMS payload formats, logo embedding, SVG
and terminal output, batch generation and every CLI subcommand.

## Limitations

- QR codes have a maximum data capacity that depends on the error
  correction level; very long text with level H may fail to fit
  (the `qrcode` library raises an error in that case).
- A logo in the centre covers part of the code, so use error
  correction level H (or at least Q) with a logo.
- SVG output is a single-colour vector code; styled module shapes
  and colours are a PNG feature.
- This version of the `qrcode` library (8.2) has no separate
  eye-pattern (finder) drawers, so the finder patterns use the
  same module shape as the rest of the code.
- QRForge encodes payloads; it cannot read a QR code back from an
  image — scanning needs a phone camera or a decoder library.

## License

MIT — see [LICENSE](LICENSE).
