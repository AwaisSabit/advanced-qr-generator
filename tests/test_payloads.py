"""Tests for payload builders: WiFi and vCard (email, phone, SMS added later)."""

import pytest

from qrforge.payloads import vcard_payload, wifi_payload


def test_wifi_wpa_payload_format():
    assert wifi_payload("MyHomeWiFi", "secret123") == "WIFI:T:WPA;S:MyHomeWiFi;P:secret123;;"


def test_wifi_wep_payload_format():
    assert wifi_payload("OldRouter", "abcde", security="WEP") == "WIFI:T:WEP;S:OldRouter;P:abcde;;"


def test_wifi_open_network_has_no_password():
    assert wifi_payload("CoffeeShop", security="nopass") == "WIFI:T:nopass;S:CoffeeShop;;"


def test_wifi_hidden_network_flag():
    payload = wifi_payload("HiddenNet", "secret123", hidden=True)
    assert payload == "WIFI:T:WPA;S:HiddenNet;P:secret123;H:true;;"


def test_wifi_special_characters_are_escaped():
    payload = wifi_payload("My;Wi:Fi", "p;ss")
    assert payload == "WIFI:T:WPA;S:My\\;Wi\\:Fi;P:p\\;ss;;"


def test_wifi_empty_ssid_is_rejected():
    with pytest.raises(ValueError):
        wifi_payload("")


def test_wifi_open_network_with_password_is_rejected():
    with pytest.raises(ValueError):
        wifi_payload("Cafe", "secret", security="nopass")


def test_wifi_secured_network_without_password_is_rejected():
    with pytest.raises(ValueError):
        wifi_payload("Home", security="WPA")


def test_wifi_unknown_security_is_rejected():
    with pytest.raises(ValueError):
        wifi_payload("Home", "secret", security="WPA3")


def test_vcard_contains_begin_and_end_markers():
    card = vcard_payload("Awais Sabit", phone="+92 300 1234567")
    assert "BEGIN:VCARD" in card
    assert "END:VCARD" in card
    assert "VERSION:3.0" in card


def test_vcard_name_fields():
    card = vcard_payload("Awais Sabit", phone="+92 300 1234567")
    assert "FN:Awais Sabit" in card
    assert "N:Sabit;Awais;;;" in card


def test_vcard_full_contact_fields():
    card = vcard_payload(
        "Awais Sabit",
        phone="+92 300 1234567",
        email="awaissabit@gmail.com",
        org="Mugazi Kitchen",
        title="Python Developer",
        url="https://github.com/AwaisSabit",
    )
    assert "TEL;TYPE=CELL:+92 300 1234567" in card
    assert "EMAIL:awaissabit@gmail.com" in card
    assert "ORG:Mugazi Kitchen" in card
    assert "TITLE:Python Developer" in card
    assert "URL:https://github.com/AwaisSabit" in card


def test_vcard_needs_name_and_contact_detail():
    with pytest.raises(ValueError):
        vcard_payload("", phone="+92 300 1234567")
    with pytest.raises(ValueError):
        vcard_payload("Awais Sabit")
