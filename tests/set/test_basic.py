# -*- coding: UTF-8 -*-
import pytest
from kuaiqu import Kuaiqu


@pytest.fixture
def dut():
    return Kuaiqu(maxsize=20, hysteresis=10, expiration=None)


def test_no_overflow(dut):

    for item in range(10):
        dut.set(item, item)

    assert len(dut) == 10

    # the oldest item
    assert dut.popitem(last=False) == (0, 0)

    # the most recent item
    assert dut.popitem() == (9, 9)


def test_on_overflow(dut):

    for item in range(25):
        dut.set(item, item)

    assert len(dut) == 15

    # the oldest item got popped
    assert dut.popitem(last=False) == (10, 10)

    # the most recent items are still there
    assert dut.popitem() == (24, 24)

