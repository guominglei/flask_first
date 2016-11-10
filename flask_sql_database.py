# -*- coding:utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy

from session import SignallingSession

db = SQLAlchemy()
Base = db.Model
db_session = db.session
