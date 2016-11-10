# -*- coding:utf-8 -*-

"""
    基本测试
"""
from flask import url_for


class TestBasic(object):

    def test_login(self, client):
        res = client.get(url_for('login'))
        assert res.status_code == 200


def test_login(client):
    res = client.get("/login/")
    assert res.status_code == 200


def test_url_login(client):
    res = client.get(url_for("login"))
    assert res.status_code == 200