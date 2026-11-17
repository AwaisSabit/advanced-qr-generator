"""Core QR code generation, built on the ``qrcode`` library.

Every QR code in QRForge is encoded here: :func:`build_qr` builds
the ``qrcode.QRCode`` object, :func:`generate_image` renders it to
a Pillow image, :func:`save_qr` writes it to a file, and
:func:`render_terminal` draws it as text for the terminal.
"""

import io
from pathlib import Path

import qrcode
from qrcode.constants import (
    ERROR_CORRECT_H,
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
)
from PIL import Image

from qrforge.models import QRConfig

ERROR_CORRECTION_LEVELS = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}

# How much of the data each level can recover after damage.
ERROR_CORRECTION_RECOVERY = {"L": "7%", "M": "15%", "Q": "25%", "H": "30%"}


def build_qr(config: QRConfig) -> qrcode.QRCode:
    """Build a ``qrcode.QRCode`` object for ``config``.

    The version is chosen automatically (``fit=True``) so the code
    grows to hold the data. Raises ``ValueError`` from
    :class:`QRConfig` for empty data or a bad correction level, and
    ``qrcode.exceptions.DataOverflowError`` when the data is too
    long even for the largest version.
    """
    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECTION_LEVELS[config.error_correction],
        box_size=config.box_size,
        border=config.border,
    )
    qr.add_data(config.data)
    qr.make(fit=True)
    return qr


def qr_matrix(config: QRConfig) -> list[list[bool]]:
    """Return the dark/light module grid for ``config``.

    ``True`` means a dark module. The grid is square and includes
    the border quiet zone.
    """
    return build_qr(config).get_matrix()


def generate_image(config: QRConfig) -> Image.Image:
    """Render ``config`` as a Pillow image (RGB mode).

    Styling (module shape, colours) is applied through
    :mod:`qrforge.styles`, so a plain square code and a styled one
    go through the same path. When ``config.logo_path`` is set, the
    logo is embedded in the centre afterwards.
    """
    from qrforge.logo import embed_logo
    from qrforge.styles import styled_image

    image = styled_image(build_qr(config), config)
    if config.logo_path:
        image = embed_logo(image, config.logo_path, config.logo_scale)
    return image


def generate_svg_text(config: QRConfig) -> str:
    """Render ``config`` as an SVG document (a string of XML).

    SVG is a single-colour vector code — infinitely scalable, ideal
    for print — so module shapes and colours do not apply here.
    """
    from qrcode.image.svg import SvgPathImage

    qr = build_qr(config)
    image = qr.make_image(image_factory=SvgPathImage)
    buffer = io.BytesIO()
    image.save(buffer)
    return buffer.getvalue().decode("utf-8")


def save_svg(config: QRConfig, output_path: str | Path) -> Path:
    """Render ``config`` and save it as an SVG file.

    Parent directories are created when needed. Returns the path
    that was written.
    """
    path = Path(output_path).with_suffix(".svg")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(generate_svg_text(config), encoding="utf-8")
    return path


def save_qr(config: QRConfig, output_path: str | Path) -> Path:
    """Render ``config`` and save it to a file.

    The format follows the file suffix: ``.svg`` writes a vector
    code, anything else writes a PNG (``.jpg``/``.bmp`` are also
    accepted and written as raster images). Parent directories are
    created when needed. Returns the path that was written.
    """
    path = Path(output_path)
    if path.suffix.lower() == ".svg":
        return save_svg(config, path)
    if path.suffix.lower() not in (".png", ".jpg", ".jpeg", ".bmp"):
        path = path.with_suffix(".png")
    path.parent.mkdir(parents=True, exist_ok=True)
    generate_image(config).save(path)
    return path


def render_terminal(config: QRConfig) -> str:
    """Draw the QR code as text blocks for the terminal.

    Each module is two characters wide so the code stays square
    in a monospace terminal. Dark modules are full blocks.
    """
    lines = []
    for row in qr_matrix(config):
        lines.append("".join("██" if cell else "  " for cell in row))
    return "\n".join(lines)


def describe_qr(config: QRConfig) -> dict:
    """Return facts about the code: version, size and capacity.

    Useful for the ``info`` command and for checking a code before
    it is saved.
    """
    qr = build_qr(config)
    matrix = qr.get_matrix()
    return {
        "data": config.data,
        "data_length": len(config.data),
        "version": qr.version,
        "error_correction": config.error_correction,
        "recovery": ERROR_CORRECTION_RECOVERY[config.error_correction],
        "modules": len(matrix),
        "box_size": config.box_size,
        "border": config.border,
        "image_size_px": len(matrix) * config.box_size,
    }
