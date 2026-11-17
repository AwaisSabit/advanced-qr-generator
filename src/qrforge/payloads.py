"""Payload builders: the exact text a QR code must hold so phones
understand it as WiFi credentials, a contact, an email, a phone
number or an SMS.

Each builder returns a plain string; :mod:`qrforge.generator`
encodes it like any other text. Keeping the formats here means the
CLI, the batch runner and library users all produce identical
payloads, and the formats are covered by tests.
"""

SECURITY_TYPES = ("WPA", "WEP", "nopass")


def _escape(value: str) -> str:
    """Escape the characters that are special in WiFi payloads.

    Backslash first, then semicolon, comma, colon and double quote.
    """
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace(":", "\\:")
        .replace('"', '\\"')
    )


def wifi_payload(
    ssid: str,
    password: str | None = None,
    security: str = "WPA",
    hidden: bool = False,
) -> str:
    """Build a WiFi payload, e.g. ``WIFI:T:WPA;S:Home;P:secret;;``.

    Phones that scan it offer to join the network. ``security`` is
    ``WPA`` (also covers WPA2/WPA3), ``WEP`` or ``nopass`` for an
    open network. ``hidden`` marks a network that does not broadcast
    its name. An open network must not carry a password, and a
    secured network must carry one.
    """
    if not ssid:
        raise ValueError("WiFi network name (SSID) must not be empty.")
    security = security.upper() if security.lower() != "nopass" else "nopass"
    if security not in SECURITY_TYPES:
        raise ValueError(
            f"WiFi security must be one of WPA, WEP or nopass, got {security!r}."
        )
    if security == "nopass" and password:
        raise ValueError("An open (nopass) network must not have a password.")
    if security in ("WPA", "WEP") and not password:
        raise ValueError(f"A {security} network needs a password.")

    parts = [f"WIFI:T:{security}", f"S:{_escape(ssid)}"]
    if password:
        parts.append(f"P:{_escape(password)}")
    if hidden:
        parts.append("H:true")
    return ";".join(parts) + ";;"
