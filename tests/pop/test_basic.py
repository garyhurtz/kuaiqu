# -*- coding: UTF-8 -*-
import string
import pytest
from kuaiqu import Kuaiqu


@pytest.fixture
def dut():
    dut = Kuaiqu(maxsize=20, hysteresis=10, expiration=None)

    for i in range(10):
        dut.set(string.ascii_lowercase[i], i)

    return dut


def test_can_pop(dut):

    val = dut.pop('a')

    assert val == 0


def test_pop_missing(dut):

    val = dut.pop('wrong')

    assert val is None

