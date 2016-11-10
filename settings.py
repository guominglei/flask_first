# -*- coding:utf-8 -*-


DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://root:@localhost/flaskr?charset=utf8mb4")
SQLALCHEMY_BINDS = {
    "slave": ("mysql+pymysql://root:@localhost/flaskr_s?charset=utf8mb4")
}
SQLALCHEMY_ECHO = True

SQLALCHEMY_POOL_SIZE = 32
SQLALCHEMY_POOL_TIMEOUT = 3
SQLALCHEMY_RECYCLE = 1800
SQLALCHEMY_MAX_OVERFLOW = 10


SECRET_KEY = "rickgml"
USERNAME = "rick"
PASSWORD = "gml"
DEBUG_TB_INTERCEPT_REDIRECTS = False
