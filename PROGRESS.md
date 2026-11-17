# QRForge — Progress

## Setup

### Done
- Created the repository layout: `src/qrforge/` (`__init__.py`,
  `__main__.py`, `cli.py`), `tests/`, `examples/`, `pyproject.toml`,
  `README.md`, `LICENSE` (MIT), `.gitignore`, `CHANGELOG.md`.
- `pyproject.toml`: version 1.0.0, Python 3.11+, dependencies
  `qrcode[pil]` and Pillow, test extra with pytest, console script
  `qrforge = "qrforge.cli:main"`, homepage
  https://github.com/AwaisSabit/advanced-qr-generator.
- Editable install in `.venv` works; `python -m qrforge` runs.

### Tests / checks run
- Command: `python -m venv .venv && .venv/bin/pip install -e ".[test]"`
- `qrcode` styled image and SVG imports verified.
- `git diff --check` — clean. No secrets in the tree; `.venv/` is ignored.

### Commits
- See `git log` for hashes. Local commits only; nothing pushed.
- The GitHub repository does not exist yet — Sir Awais creates the
  empty public repo `advanced-qr-generator` himself, then the
  commits are pushed to it.

## Version 1.0.0 — 2026-11-17

### Done (12 commits, one feature each)
1. Project setup: package layout, pyproject, README, gitignore.
2. Core QR generation for text and URLs with error correction L/M/Q/H.
3. Styled codes: colours and module shapes (square, rounded, dots,
   gapped, bars) through `StyledPilImage`.
4. WiFi payloads: WPA, WEP, open networks, hidden SSID, escaping.
5. vCard 3.0 contact payloads.
6. Email (`mailto:`), phone (`tel:`) and SMS (`sms:`) payloads.
7. Logo embedding in the centre, on a white rounded backing.
8. SVG (valid XML) and terminal output alongside PNG.
9. Batch generation from CSV and JSON, one file per row.
10. CLI with `generate`, `wifi`, `vcard`, `email`, `phone`, `sms`,
    `batch` and `info` subcommands.
11. Tests for generation, WiFi, vCard, styling and the CLI.
12. Documentation, examples (`examples/demo.py`, `examples/sample.csv`)
    and final polish for version 1.0.0.

Two real bugs found and fixed while testing, before finishing:
1. `qrcode` 8.2 has no `qrcode.image.styles.eyedrawers` module —
   eye-pattern styling was dropped; finder patterns use the module
   shape instead.
2. `SolidFillColorMask` needs RGB tuples, not colour names — passing
   `"black"` produced a broken 5-tuple paint colour. Colours are now
   converted with `Pillow`'s `ImageColor.getrgb` first.

### Tests / checks run (final)
- `.venv/bin/python -m pytest -q` → **69 passed**.
- `qrforge generate`, `wifi`, `vcard` and `batch` verified by hand
  (PNG and SVG files written, SVG parsed as XML, terminal output
  drawn, `info` reporting version 2, 33x33 modules for a URL).
- `python examples/demo.py` — writes `examples/output/` with a
  plain, a styled logo, a WiFi and a vCard PNG plus an SVG.
- `git diff --check` — clean. No secrets in the tree; `.venv/` is
  ignored. Working tree clean; nothing pushed (no remote yet).
