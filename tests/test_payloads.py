"""Tests for payload builders: WiFi (vCard, email, phone, SMS added later)."""

import pytest

from qrforge.payloads import wifi_payload


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
