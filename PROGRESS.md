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
