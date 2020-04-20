# -*- coding: UTF-8 -*-
import pytest
from kuaiqu import Kuaiqu


@pytest.fixture
def dut():
    dut = Kuaiqu(maxsize=20, hysteresis=10, expiration=None)
    dut.set(u'key', u'value')
    return dut


def test_get_key_exists(dut):
    assert dut.get(u'key') == u'value'


def test_get_key_doest_exist(dut):
    assert dut.get(u'doesnt_exist') is None


def test_getitem_key_exists(dut):
    assert dut[u'key'] == u'value'


def test_getitem_key_doest_exist(dut):
    assert dut[u'doesnt_exist'] is None
