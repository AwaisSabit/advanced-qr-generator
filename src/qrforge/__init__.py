"""QRForge — an advanced QR code generator.

Build styled, branded and payload-specific QR codes (text, URLs, WiFi,
contacts, email, phone and SMS) with the ``qrcode`` library and Pillow.

Library example::

    from qrforge import QRConfig, save_qr
    from qrforge.payloads import wifi_payload

    config = QRConfig(wifi_payload("MyHomeWiFi", "secret123"),
                      error_correction="H", module_shape="rounded")
    save_qr(config, "wifi.png")
"""

from qrforge.generator import describe_qr, generate_image, render_terminal, save_qr
from qrforge.models import QRConfig
from qrforge.payloads import (
    email_payload,
    phone_payload,
    sms_payload,
    vcard_payload,
    wifi_payload,
)

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "QRConfig",
    "describe_qr",
    "generate_image",
    "render_terminal",
    "save_qr",
    "email_payload",
    "phone_payload",
    "sms_payload",
    "vcard_payload",
    "wifi_payload",
]
