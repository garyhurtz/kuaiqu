# -*- coding: UTF-8 -*-
import pytest

from kuaiqu import Kuaiqu


@pytest.fixture
def dut():
    dut = Kuaiqu(maxsize=20, hysteresis=10, expiration=None)
    dut.set("key", "value")
    return dut


def test_clear(dut):

    assert len(dut) == 1

    dut.clear()

    assert len(dut) == 0
