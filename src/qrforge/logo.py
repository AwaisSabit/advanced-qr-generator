"""Logo embedding: place a small image in the centre of a QR code.

The logo covers the middle modules, so codes with a logo should
use error correction level Q or H — the code can then still be
read even with the centre covered. The logo is drawn on a white
rounded backing so it stays visible on dark or coloured codes.
"""

from pathlib import Path

from PIL import Image, ImageDraw


def embed_logo(image: Image.Image, logo_path: str | Path, scale: float = 0.2) -> Image.Image:
    """Return a copy of ``image`` with ``logo_path`` pasted in the centre.

    ``scale`` is the logo width as a fraction of the QR code width
    (0.2 means the logo is a fifth of the code wide). Raises
    ``FileNotFoundError`` when the logo file does not exist and
    ``ValueError`` for a scale outside 0–0.3.
    """
    path = Path(logo_path)
    if not path.exists():
        raise FileNotFoundError(f"Logo file not found: {path}")
    if not 0 < scale <= 0.3:
        raise ValueError("Logo scale must be between 0 and 0.3.")

    result = image.convert("RGBA")
    logo = Image.open(path).convert("RGBA")

    logo_width = int(result.width * scale)
    ratio = logo_width / logo.width
    logo = logo.resize(
        (logo_width, max(1, int(logo.height * ratio))), Image.Resampling.LANCZOS
    )

    # White rounded backing, slightly larger than the logo, so the
    # logo reads clearly against any code colour.
    pad = max(4, logo_width // 12)
    backing = Image.new(
        "RGBA",
        (logo.width + 2 * pad, logo.height + 2 * pad),
        (255, 255, 255, 255),
    )
    mask = Image.new("L", backing.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, backing.width - 1, backing.height - 1],
        radius=pad,
        fill=255,
    )
    x = (result.width - backing.width) // 2
    y = (result.height - backing.height) // 2
    result.paste(backing, (x, y), mask)
    result.paste(logo, (x + pad, y + pad), logo)
    return result.convert("RGB")
