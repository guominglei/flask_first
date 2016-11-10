# -*- coding:utf-8 -*-


import pytest
from flaskr import app as fl_app


@pytest.fixture
def app():
    app = fl_app
    return app