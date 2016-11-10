# -*- coding:utf-8 -*-

"""
    延时回调 指的是再当前请求view方法处理结束后，再进行的后续特殊处理。
    实现方法就是在环境变量g中注册回调事件。然后挂载到after_request 事件上。

    延时回调。
    1、是针对所有请求的吗? 不是针对所有请求的。可以定制化。
    2、延时回调可以理解为中间件process_response。
    3、延时回调的数据是如何传递的？就像下边的例子中language是如何传递的？

    延时回调是针对
"""
from flask import g
from flask import request

# 定义注册修饰器 在实际view中注册某个回调事件


def after_this_request(func):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(func)
    print len(g.after_request_callbacks)
    return func

# 定义 after_request 事件
#@app.after_request 实际应用中使用


def call_after_reqeust_callbacks(response):

    for callback in getattr(g, "after_request_callbacks", ()):
        print "yy"
        callback(response)
    return response


# view中如何使用
#@app.before_request
def detect_user_language():
    print "xx"
    language = request.cookies.get("bf", None)
    if language is None:
        language = "baofeng"

        @after_this_request
        def remember_language(response):
            response.set_cookie("bf", language)  # language 如何获取到的
    g.language = language
