# -*- coding: UTF-8 -*-
import pytest

from kuaiqu import Kuaiqu


@pytest.fixture
def dut():
    dut = Kuaiqu(maxsize=20, hysteresis=10, expiration=None)
    dut.set("key", "value")
    return dut


def test_contains(dut):
    assert "key" in dut


def test_not_contains(dut):
    assert "wrong" not in dut
