# -*- coding:utf-8 -*-

"""
    公用修饰器
"""
from flask import session
from flask import abort
from functools import wraps


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if session.get("username", None):
            print "login"
            return func(*args, **kwargs)
        else:
            print "not login"
            abort(401)

    return wrapper