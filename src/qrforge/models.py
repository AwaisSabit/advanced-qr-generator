"""Data models for QRForge: the settings that describe one QR code."""

from dataclasses import dataclass


@dataclass
class QRConfig:
    """Settings for a single QR code.

    ``data`` is the text encoded in the code. ``error_correction``
    is one of ``L`` (7% recovery), ``M`` (15%), ``Q`` (25%) or
    ``H`` (30%). Higher levels survive more damage but hold less
    data. ``box_size`` is the pixel size of one module, ``border``
    is the quiet-zone width in modules. ``fill_color`` and
    ``back_color`` are any Pillow colour (name or ``#rrggbb``).
    ``module_shape`` is one of ``square``, ``rounded``, ``dots``,
    ``gapped``, ``bars`` or ``bars-horizontal``
    (see :mod:`qrforge.styles`).
    """

    data: str
    error_correction: str = "M"
    box_size: int = 10
    border: int = 4
    fill_color: str = "black"
    back_color: str = "white"
    module_shape: str = "square"
    logo_path: str | None = None
    logo_scale: float = 0.2

    def __post_init__(self):
        if not self.data:
            raise ValueError("QR code data must not be empty.")
        if self.error_correction not in ("L", "M", "Q", "H"):
            raise ValueError(
                "Error correction must be one of L, M, Q or H, "
                f"got {self.error_correction!r}."
            )
        if self.box_size < 1:
            raise ValueError("Box size must be at least 1.")
        if self.border < 0:
            raise ValueError("Border must not be negative.")
        if not 0 < self.logo_scale <= 0.3:
            raise ValueError("Logo scale must be between 0 and 0.3.")
        if self.module_shape not in (
            "square", "rounded", "dots", "gapped", "bars", "bars-horizontal",
        ):
            raise ValueError(f"Unknown module shape: {self.module_shape!r}.")

