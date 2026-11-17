"""Payload builders: the exact text a QR code must hold so phones
understand it as WiFi credentials, a contact, an email, a phone
number or an SMS.

Each builder returns a plain string; :mod:`qrforge.generator`
encodes it like any other text. Keeping the formats here means the
CLI, the batch runner and library users all produce identical
payloads, and the formats are covered by tests.
"""

SECURITY_TYPES = ("WPA", "WEP", "nopass")


def _vcard_name_parts(full_name: str) -> tuple[str, str]:
    """Split ``"First Last"`` into ``(first, last)`` for the ``N:`` field.

    A single word is treated as the family name. Middle names stay
    with the first name.
    """
    words = full_name.split()
    if len(words) == 1:
        return "", words[0]
    return " ".join(words[:-1]), words[-1]


def vcard_payload(
    name: str,
    phone: str | None = None,
    email: str | None = None,
    org: str | None = None,
    title: str | None = None,
    url: str | None = None,
    address: str | None = None,
    note: str | None = None,
) -> str:
    """Build a vCard 3.0 payload for a contact QR code.

    Phones that scan it offer to save the contact. ``name`` is
    required, plus at least one of ``phone`` or ``email`` so the
    card is useful. Lines use CRLF, as the vCard format specifies.
    """
    if not name or not name.strip():
        raise ValueError("A vCard needs a name.")
    if not phone and not email:
        raise ValueError("A vCard needs at least a phone number or an email address.")

    first, last = _vcard_name_parts(name.strip())
    lines = ["BEGIN:VCARD", "VERSION:3.0", f"N:{last};{first};;;", f"FN:{name.strip()}"]
    if org:
        lines.append(f"ORG:{org}")
    if title:
        lines.append(f"TITLE:{title}")
    if phone:
        lines.append(f"TEL;TYPE=CELL:{phone}")
    if email:
        lines.append(f"EMAIL:{email}")
    if url:
        lines.append(f"URL:{url}")
    if address:
        lines.append(f"ADR:;;{address};;;;")
    if note:
        lines.append(f"NOTE:{note.replace(chr(10), ' ')}")
    lines.append("END:VCARD")
    return "\r\n".join(lines)


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
