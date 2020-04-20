# -*- coding: UTF-8 -*-
import pytest
from kuaiqu import Kuaiqu
import time


@pytest.fixture
def dut():
    dut = Kuaiqu(rolling=1./240)  # 0.25 seconds
    dut.set(u'key', u'value')
    return dut


def test_get_immediately(dut):
    assert dut.get(u'key') == u'value'


def test_wait_then_get(dut):
    time.sleep(1)
    assert dut.get(u'key') is None

