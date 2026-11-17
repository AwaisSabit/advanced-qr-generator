"""Demo script: generate one of each QRForge code type.

Run from the repository root after installing the project:

    python examples/demo.py

It writes PNG and SVG files into ``examples/output/`` and prints a
terminal QR code. A small demo logo is drawn with Pillow, so the
script needs no extra files.
"""

from pathlib import Path

from PIL import Image, ImageDraw

from qrforge import QRConfig, save_qr
from qrforge.generator import generate_svg_text, render_terminal, save_svg
from qrforge.payloads import vcard_payload, wifi_payload

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)


def make_demo_logo(path: Path) -> Path:
    """Draw a small red square logo with white initials."""
    logo = Image.new("RGB", (200, 200), (220, 30, 30))
    draw = ImageDraw.Draw(logo)
    draw.text((70, 85), "QF", fill="white")
    logo.save(path)
    return path


def main() -> None:
    logo = make_demo_logo(OUT / "demo-logo.png")

    plain = save_qr(QRConfig("https://example.com"), OUT / "website.png")
    print(f"Text/URL code: {plain}")

    styled = save_qr(
        QRConfig(
            "https://github.com/AwaisSabit",
            error_correction="H",
            fill_color="#1a5276",
            module_shape="rounded",
            logo_path=str(logo),
        ),
        OUT / "github-styled-logo.png",
    )
    print(f"Styled code with logo: {styled}")

    wifi = save_qr(
        QRConfig(wifi_payload("MyHomeWiFi", "secret123"), error_correction="H"),
        OUT / "wifi.png",
    )
    print(f"WiFi code: {wifi}")

    contact = save_qr(
        QRConfig(
            vcard_payload(
                "Awais Sabit",
                phone="+92 300 1234567",
                email="awaissabit@gmail.com",
                org="Mugazi Kitchen",
            )
        ),
        OUT / "contact.png",
    )
    print(f"vCard code: {contact}")

    vector = save_svg(QRConfig("https://example.com"), OUT / "website.svg")
    print(f"SVG code: {vector} ({len(generate_svg_text(QRConfig('https://example.com')))} chars of XML)")

    print()
    print("Terminal code for https://example.com:")
    print(render_terminal(QRConfig("https://example.com")))


if __name__ == "__main__":
    main()
