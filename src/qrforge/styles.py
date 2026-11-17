"""Styling for QR codes: colours, module shapes and eye shapes.

Styling is rendered with ``qrcode``'s ``StyledPilImage`` factory, so
the encoding stays exactly the same — only the look changes. A code
styled with dots or rounded modules still scans like the plain one.
"""

from PIL import ImageColor
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import (
    CircleModuleDrawer,
    GappedSquareModuleDrawer,
    HorizontalBarsDrawer,
    RoundedModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
)

MODULE_DRAWERS = {
    "square": SquareModuleDrawer,
    "rounded": RoundedModuleDrawer,
    "dots": CircleModuleDrawer,
    "gapped": GappedSquareModuleDrawer,
    "bars": VerticalBarsDrawer,
    "bars-horizontal": HorizontalBarsDrawer,
}

def validate_color(color: str) -> tuple[int, int, int]:
    """Check that ``color`` is a Pillow colour name or ``#rrggbb`` value.

    Returns the colour as an ``(r, g, b)`` tuple — the form the
    ``qrcode`` colour mask needs (it does not accept colour names).
    Raises ``ValueError`` for anything Pillow cannot understand, so
    a typo fails fast instead of producing a broken image.
    """
    try:
        return ImageColor.getrgb(color)
    except ValueError:
        raise ValueError(f"Not a valid colour: {color!r}.") from None


def get_module_drawer(name: str):
    """Return the module drawer class for ``name``."""
    try:
        return MODULE_DRAWERS[name]
    except KeyError:
        raise ValueError(
            f"Unknown module shape {name!r}. "
            f"Choose one of: {', '.join(sorted(MODULE_DRAWERS))}."
        ) from None


def styled_image(qr, config):
    """Render an already-built ``qrcode.QRCode`` as a styled image.

    Uses the module shape from ``config`` and a solid colour mask
    for the fill and background colours. (This version of the
    ``qrcode`` library has no separate eye-pattern drawers, so the
    finder patterns use the same module shape.)
    """
    image = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=get_module_drawer(config.module_shape)(),
        color_mask=SolidFillColorMask(
            back_color=validate_color(config.back_color),
            front_color=validate_color(config.fill_color),
        ),
    )
    return image.convert("RGB")
