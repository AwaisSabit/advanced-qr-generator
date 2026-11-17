"""Command line interface for QRForge.

Subcommands
-----------
``generate``  a QR code for text or a URL
``wifi``      a WiFi network code
``vcard``     a contact (vCard) code
``email``     an email code (``mailto:``)
``phone``     a phone-call code (``tel:``)
``sms``       a text-message code (``sms:``)
``batch``     many codes at once from a CSV or JSON file
``info``      facts about the code a piece of data would produce

Every code subcommand takes the same styling options: error
correction level, colours, module shape, logo, box size and
border. The output format follows the output file suffix
(``.svg`` for vector, anything else for PNG); with no ``--output``
the code is drawn in the terminal instead.
"""

import argparse
import sys

from qrforge import __version__
from qrforge.batch import run_batch
from qrforge.generator import describe_qr, render_terminal, save_qr
from qrforge.models import QRConfig
from qrforge.payloads import (
    email_payload,
    phone_payload,
    sms_payload,
    vcard_payload,
    wifi_payload,
)
from qrforge.styles import MODULE_DRAWERS


def _add_style_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--error-correction",
        default="M",
        choices=["L", "M", "Q", "H"],
        help="error correction level: L (7%%), M (15%%), Q (25%%) or H (30%%) (default: M)",
    )
    parser.add_argument("--box-size", type=int, default=10,
                        help="pixel size of one module (default: 10)")
    parser.add_argument("--border", type=int, default=4,
                        help="quiet-zone width in modules (default: 4)")
    parser.add_argument("--fill", default="black",
                        help="module colour, name or #rrggbb (default: black)")
    parser.add_argument("--back", default="white",
                        help="background colour, name or #rrggbb (default: white)")
    parser.add_argument("--shape", default="square", choices=sorted(MODULE_DRAWERS),
                        help="module shape (default: square)")
    parser.add_argument("--logo", default=None,
                        help="image file to embed in the centre of the code")
    parser.add_argument("--logo-scale", type=float, default=0.2,
                        help="logo width as a fraction of the code width, up to 0.3 (default: 0.2)")
    parser.add_argument("--output", "-o", default=None,
                        help="file to write (.svg for vector, otherwise PNG)")


def _config_from_args(args, data: str) -> QRConfig:
    return QRConfig(
        data,
        error_correction=args.error_correction,
        box_size=args.box_size,
        border=args.border,
        fill_color=args.fill,
        back_color=args.back,
        module_shape=args.shape,
        logo_path=args.logo,
        logo_scale=args.logo_scale,
    )


def _emit(args, data: str) -> int:
    """Save the code to ``--output`` or draw it in the terminal."""
    config = _config_from_args(args, data)
    if args.output:
        path = save_qr(config, args.output)
        print(f"Saved QR code to {path}")
    else:
        print(render_terminal(config))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qrforge", description="Advanced QR code generator."
    )
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="QR code for text or a URL.")
    gen.add_argument("data", help="text or URL to encode")
    _add_style_args(gen)

    wifi = sub.add_parser("wifi", help="QR code for a WiFi network.")
    wifi.add_argument("--ssid", required=True, help="network name")
    wifi.add_argument("--password", default=None, help="network password")
    wifi.add_argument("--security", default="WPA",
                      choices=["WPA", "WEP", "nopass"],
                      help="security type (default: WPA)")
    wifi.add_argument("--hidden", action="store_true",
                      help="the network does not broadcast its name")
    _add_style_args(wifi)

    card = sub.add_parser("vcard", help="QR code for a contact (vCard).")
    card.add_argument("--name", required=True, help="full name, e.g. 'Awais Sabit'")
    card.add_argument("--phone", default=None)
    card.add_argument("--email", default=None)
    card.add_argument("--org", default=None, help="organisation")
    card.add_argument("--title", default=None, help="job title")
    card.add_argument("--url", default=None)
    card.add_argument("--address", default=None)
    card.add_argument("--note", default=None)
    _add_style_args(card)

    mail = sub.add_parser("email", help="QR code that opens a new email.")
    mail.add_argument("address", help="email address")
    mail.add_argument("--subject", default=None)
    mail.add_argument("--body", default=None)
    _add_style_args(mail)

    phone = sub.add_parser("phone", help="QR code that dials a number.")
    phone.add_argument("number", help="phone number")
    _add_style_args(phone)

    sms = sub.add_parser("sms", help="QR code that opens a text message.")
    sms.add_argument("number", help="phone number")
    sms.add_argument("--message", default=None)
    _add_style_args(sms)

    batch = sub.add_parser("batch", help="QR codes from a CSV or JSON file.")
    batch.add_argument("input", help="CSV or JSON file with one code per row")
    batch.add_argument("--output-dir", default="generated",
                       help="directory for the codes (default: generated)")

    info = sub.add_parser("info", help="Facts about a QR code for some data.")
    info.add_argument("data", help="text or URL to inspect")
    info.add_argument("--error-correction", default="M", choices=["L", "M", "Q", "H"])
    return parser


def main(argv=None) -> int:
    """Entry point for the ``qrforge`` command. Returns an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "generate":
            return _emit(args, args.data)
        if args.command == "wifi":
            return _emit(
                args,
                wifi_payload(args.ssid, args.password, args.security, args.hidden),
            )
        if args.command == "vcard":
            return _emit(
                args,
                vcard_payload(
                    args.name, args.phone, args.email, args.org,
                    args.title, args.url, args.address, args.note,
                ),
            )
        if args.command == "email":
            return _emit(args, email_payload(args.address, args.subject, args.body))
        if args.command == "phone":
            return _emit(args, phone_payload(args.number))
        if args.command == "sms":
            return _emit(args, sms_payload(args.number, args.message))
        if args.command == "batch":
            written = run_batch(args.input, args.output_dir)
            for path in written:
                print(f"Saved QR code to {path}")
            print(f"Generated {len(written)} QR code(s) in {args.output_dir}")
            return 0
        if args.command == "info":
            config = QRConfig(args.data, error_correction=args.error_correction)
            info = describe_qr(config)
            print(f"Data: {info['data']}")
            print(f"Data length: {info['data_length']} characters")
            print(f"QR version: {info['version']}")
            print(f"Error correction: {info['error_correction']} "
                  f"({info['recovery']} recovery)")
            print(f"Modules: {info['modules']} x {info['modules']}")
            print(f"Image size: {info['image_size_px']} x {info['image_size_px']} px")
            return 0
    except (ValueError, FileNotFoundError) as exc:
        print(f"qrforge: error: {exc}", file=sys.stderr)
        return 2
    return 2
