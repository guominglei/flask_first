# -*- coding:utf-8 -*-

"""
    view 类
"""
from flask import render_template, request, Response
from flask.views import View, MethodView
from flask import json
from decorator import login_required
from models import Entries


class ShowEntiesView(View):

    methods = ["GET"]
    decorators = [login_required]

    def get_template_name(self):

        return "show_list.html"

    def render_template(self, context):

        return render_template(self.get_template_name(), **context)

    def get_data(self):
        items = Entries.get_list()
        return items

    def dispatch_request(self, *args, **kwargs):
        """
            实例化
            具体请求处理方法
        """
        entry_list = self.get_data()
        context = {"entries": entry_list}
        return self.render_template(context)


class EntiesApi(MethodView):
    """
        主要用于api操作。
        根据http 的method 不同。使用不同的方法。

        /users/	GET	给出一个包含所有用户的列表
        /users/	POST	创建一个新用户
        /users/<id>	GET	显示一个用户
        /users/<id>	PUT	更新一个用户
        /users/<id>	DELETE	删除一个用户

    """

    decorators = [] #方法的修饰器

    def create_response(self, results):
        print results
        response = Response(json.dumps(results),
                            content_type="application/json; charset=utf-8")
        return response

    def get(self, enty_id):

        if enty_id is None:
            items = Entries.get_list(format=True)
        else:
            items = Entries.query.get(enty_id)
            items = items.format()
        results = {
            "status": True,
            "data": items,
        }

        return self.create_response(results)

    def post(self):

        title = request.form.get("title", None)
        text = request.form.get("text", None)

        Entries.new_item(title, text)

        results = {
            "status": True,
        }

        return self.create_response(results)

    def delete(self, enty_id):

        if enty_id is not None:

            status = Entries.delete_item(enty_id=enty_id)

            results = {
                "status": status
            }

        return self.create_response(results)

    def put(self, enty_id):

        title = request.form.get("title", None)
        text = request.form.get("text", None)

        status = Entries.update_item(enty_id, title=title, text=text)

        results = {
            "status": status
        }

        return self.create_response(results)
