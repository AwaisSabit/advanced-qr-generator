"""Allow ``python -m qrforge`` to run the command line interface."""

from qrforge.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
