# -*- coding:utf8 -*-

"""
    views
"""
from flask import (
    Flask, render_template, session, request,
    Response, abort, url_for, flash, redirect, g
)
from flask_debugtoolbar import DebugToolbarExtension


from models import Entries
from user.views import user
from flask_sql_database import db_session, db
from view_class import ShowEntiesView, EntiesApi
from lazy_callback import (
    detect_user_language, call_after_reqeust_callbacks
)


# 配置文件

# 初始化

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")

    toolbar = DebugToolbarExtension(app)

    # 日志
    import logging
    file_handler = logging.FileHandler("/tmp/flask_test.log")
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    db.init_app(app)

    return app

app = create_app()

# 中间件相关概念
# 1 请求处理前 before_request
# 2 请求处理后 after_request
# 3 异常发生处理 teardown_request


@app.before_request
def before_request():
    # g这个对象与每一个请求是一一对应的，并且只在函数内部有效。
    # 不要在其它对象中储存类似信息，因为在多线程环境下无效。
    # 这个特殊的 g对象会在后台神奇的工作，保证系统正常运行。

    #g.db = engine.connect()
    pass
# 挂载延时回调
app.before_request(detect_user_language)


@app.after_request
def after_request(response):
    response.headers["ha"] = "HH"
    return response
# 挂载延时回调
app.after_request(call_after_reqeust_callbacks)


@app.teardown_request
def teardown_request(exception):
    pass

# app 结束后关闭连接


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# 视图方法
@app.route("/")
def show_entries():

    app.logger.info("HHH")
    entry_list = Entries.get_list()

    return render_template("show_list.html", entries=entry_list)


@app.route("/add/", methods=["POST"])
def add_entry():

    if not session.get("username", None):
        abort(401)

    title = request.form.get("title", None)
    text = request.form.get("text", None)

    Entries.new_item(title, text)

    flash(u"添加成功")

    return redirect(url_for("show_entries"))


@app.route("/login/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":
        username = request.form.get("username", None)
        pw = request.form.get("password", None)

        if username != app.config.get("USERNAME", None):
            error = u"用户名不对"
        elif pw != app.config.get("PASSWORD", None):
            error = u"密码不对"
        else:
            session["username"] = username
            flash(u"登录成功！")
            return redirect(url_for("show_entries"))

    data = render_template("login.html", error=error)

    return data


@app.route("/logout/")
def logout():

    session.pop("username", None)

    flash(u"登出成功！")

    return redirect(url_for("/login/"))


# 处理异常
@app.errorhandler(401)
def deal_401(error):
    # error is werkzeug.exceptions.xx
    print error.code
    # return u"请您登录后在操作", error.code
    return redirect(url_for("login"))


##############
app.add_url_rule('/class_view/', view_func=ShowEntiesView.as_view('classview'))


################
# api
def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET', ])
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

register_api(EntiesApi, 'enty_api', '/enties/', pk='enty_id')


#################
# blueprint 蓝图 挂载蓝图
# 假如在注册的时候定义前缀。实际定义中的前缀会被覆盖
app.register_blueprint(user, url_prefix='/user_profile')


if __name__ == "__main__":
    # flask_sql调用这个
    # db.init_app(app)
    #
    app.run()
