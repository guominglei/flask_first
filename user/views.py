# -*- coding:utf-8 -*-

"""
    用户相关的视图方法。
    利用蓝图(blueprint)

    @user.route("/about/")   url 就是全称。
"""
import os
import sys

from flask import Blueprint, render_template, request, Response, jsonify
from flask.views import MethodView
from .models import User

CURENTPATH = os.path.abspath(os.path.dirname(__file__))

user = Blueprint('user',
                 __name__,
                 template_folder=os.path.join(CURENTPATH, "templates"),  # 模板地址
                 static_folder=os.path.join(CURENTPATH, "static"),  # 静态文件地址
                 url_prefix='/users',  # url前缀  注意假如在注册的时候定义前缀。这里定义的前缀会被覆盖
                 )


@user.route("/about/")
def about():
    return render_template("about.html")


# view class
class UserApi(MethodView):
    """
        主要用于api操作。
        根据http 的method 不同。使用不同的方法。

        /users/	GET	给出一个包含所有用户的列表
        /users/	POST	创建一个新用户
        /users/<id>	GET	显示一个用户
        /users/<id>	PUT	更新一个用户
        /users/<id>	DELETE	删除一个用户

    """

    decorators = []  # 方法的修饰器

    def get(self, user_id):

        if user_id is None:
            items = User.get_list(format=True)
        else:
            items = User.query.get(user_id)
            items = items.format()
        results = {
            "status": True,
            "data": items,
        }

        return jsonify(results)

    def post(self):

        name = request.form.get("name", "")
        if name:
            name = name.strip()
        age = request.form.get("age", None)
        password = request.form.get("password", None)
        salary = request.form.get("salary", None)
        admin = request.form.get("admin", "False")
        admin = eval(admin)
        User.new_item(name, age, password, salary, admin=admin)
        results = {
            "status": True,
        }

        return jsonify(results)

    def delete(self, user_id):

        if user_id is not None:

            status = User.delete_item(user_id=user_id)

            results = {
                "status": status
            }

        return jsonify(results)

    def put(self, user_id):

        name = request.form.get("name", None)
        age = request.form.get("age", None)

        status = User.update_item(user_id, name=name, age=age)

        results = {
            "status": status
        }

        return jsonify(results)

# api


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    user.add_url_rule(url, defaults={pk: None},
                      view_func=view_func, methods=['GET', ])
    user.add_url_rule(url, view_func=view_func, methods=['POST', ])
    user.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                      methods=['GET', 'PUT', 'DELETE'])

register_api(UserApi, 'user_api', '/users/', pk='user_id')
