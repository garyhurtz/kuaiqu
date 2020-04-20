# -*- coding: UTF-8 -*-
import string
import pytest
from kuaiqu import Kuaiqu
from collections import OrderedDict


@pytest.fixture
def dut():
    dut = Kuaiqu(maxsize=20, hysteresis=10, expiration=None)

    for i in range(10):
        dut.set(string.ascii_lowercase[i], i)

    return dut


def test_can_iterate(dut):

    for key in dut.keys():
        assert isinstance(key, str)


