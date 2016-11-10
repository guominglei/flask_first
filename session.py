# -*- coding:utf-8 -*-

import flask
from flask.ext.sqlalchemy import (
    SignallingSession as _SignallingSession, SessionBase, get_state
)


class SignallingSession(_SignallingSession):
    def __init__(self, *args, **kwargs):
        _SignallingSession.__init__(self, *args, **kwargs)
        self._name = None

    def using_bind(self, name):
        self._name = name
        return self

    def get_bind(self, mapper, clause=None):

        # 获取bind首先以模型定义时候的__bind_key__ 为先。
        # 其次才是人为定义的

        if mapper is not None:
            info = getattr(mapper.mapped_table, "info", {})
            bind_key = self._name or info.get("bind_key")

        else:
            bind_key = self._name

        if bind_key is not None:
            state = get_state(self.app)
            return state.db.get_engine(self.app, bind=bind_key)
        else:
            return SessionBase.get_bind(self, mapper, clause)

# 动态替换类，没有使用过。
flask.ext.sqlalchemy.SignallingSession = SignallingSession