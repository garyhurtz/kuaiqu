# -*- coding: UTF-8 -*-
import pytest

from kuaiqu import Kuaiqu


@pytest.fixture
def dut():
    dut = Kuaiqu(maxsize=20, hysteresis=10, expiration=None)
    dut.set("key", "value")
    return dut


def test_get_key_exists(dut):
    assert dut.get("key") == "value"


def test_get_key_doest_exist(dut):
    assert dut.get("doesnt_exist") is None


def test_getitem_key_exists(dut):
    assert dut["key"] == "value"


def test_getitem_key_doest_exist(dut):
    assert dut["doesnt_exist"] is None
