"""Command line interface for QRForge (placeholder for the first commit).

The full subcommand interface (generate, wifi, vcard, batch, info)
is added in a later step; this stub keeps ``python -m qrforge`` and
the ``qrforge`` console script importable from the start.
"""

from qrforge import __version__


def main(argv=None):
    """Entry point for the ``qrforge`` command."""
    print(f"qrforge {__version__} — advanced QR code generator")
    print("Run `qrforge --help` once the subcommands are added.")
    return 0
