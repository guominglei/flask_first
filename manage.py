# -*- coding:utf-8 -*-
"""
    通过flask-script 扩展 自定义管理命令
    生成命令方法
    1、manager.command修饰器
    2、manager.option修饰器
    3、继承command
"""
from flask.ext.script import (
    Manager, prompt_bool, Server, Command, Option, Shell,
    prompt, prompt_pass, prompt_choices
)

import models
from .flaskr import app

manager = Manager(app)

# 注册命令
manager.add_command("runserver", Server(host="localhost", port="8888"))

# 定义命令方式1


@manager.command
def command_test(host, port):  # 没有默认值 没有参数名称

    print "host:{}\tport:{}".format(host, port)

# 定义方式2
# dest 参数名称


@manager.option(
    '-h',
    '--host',
    dest="host",
    default="localhost",
    help=u"服务器地址")
@manager.option("-p", "--port", dest="port", default="7777", help="端口号")
def command_test_default(host, port):  # 有参数名称 有默认值
    msg = "host:{}\tport:{}".format(host, port)
    if prompt_bool(msg):  # 用户交互
        print "You input {}".format(msg)
        info = prompt("you name")
        print "info:{}".format(info)
        password = prompt_pass("password")
        print "password:{}".format(password)
        # China [1], USA [2])  选择 1，2
        #(key, value)
        choice = prompt_choices(u"homeland", (("1", "China"), ("2", "USA")))
        print "choice:{}".format(choice)
    else:
        print "out"


####################################
# 方式3 先定义 然后注册
class HelloWold(Command):
    "print hello world doc"
    print "hello world"
    option_list = (
        Option('--name', "-n", dest="username", default="rick", help=u"用户名"),
    )

    def run(self, username):
        print u"hello {} welcome to 靠山屯".format(username)

manager.add_command("hello", HelloWold())

########################################


#############
# shell
def _make_context():
    return dict(app=app, models=models)

manager.add_command("shell", Shell(make_context=_make_context))


if __name__ == "__main__":

    manager.run()
