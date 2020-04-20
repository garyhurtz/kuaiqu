# -*- coding: UTF-8 -*-
import pytest
from kuaiqu import Kuaiqu


@pytest.fixture
def dut():
    dut = Kuaiqu(maxsize=20, hysteresis=10, expiration=None)
    dut.set(u'key', u'value')
    return dut


def test_delete_key_exists(dut):
    assert dut.delete(u'key') is None


def test_delete_key_doesnt_exist(dut):
    assert dut.delete(u'wrong') is None


def test_delete_item_key_exists(dut):
    # doesnt raise
    del dut[u'key']


def test_delete_item_key_doesnt_exist(dut):
    # doesnt raise
    del dut[u'key']

