# -*- coding: UTF-8 -*-
import time

import pytest

from kuaiqu import Kuaiqu


@pytest.fixture
def dut():
    dut = Kuaiqu(expiration=1.0 / 240)  # 0.25 seconds
    dut.set("key", "value")
    return dut


def test_get_immediately(dut):
    assert dut.get("key") == "value"


def test_wait_then_get(dut):
    time.sleep(1)
    assert dut.get("key") is None
