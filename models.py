# -*- coding:utf-8 -*-

"""
    模型
"""
import traceback
from sqlalchemy import Column, Integer, String, Text

from .flask_sql_database import Base, db_session


class Entries(Base):

    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    text = Column(Text)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return "<Entry {}>".format(self.id)

    def __str__(self):
        return self.title

    def format(self):

        info = {
            "title": self.title,
            "text": self.text,
        }

        return info

    @classmethod
    def get_list(cls, format=False):

        items = cls.query.all()

        #items = db_session().bind("slave").query(cls).all()
        if format:
            items = [item.format() for item in items]
        return items

    @classmethod
    def new_item(cls, title, text):
        item = cls(title, text)
        db_session.add(item)
        db_session.commit()

    @classmethod
    def delete_item(cls, enty_id):

        status = False
        try:
            item = cls.query.get(enty_id)
            db_session.delete(item)
            db_session.commit()
            status = True
        except Exception as e:
            print traceback.format_exc()

        return status

    @classmethod
    def update_item(cls, enty_id, title=title, text=text):

        status = False
        try:
            item = cls.query.get(enty_id)
            if title:
                item.title = title
            if text:
                item.text = text
            db_session.add(item)
            db_session.commit()
            status = True
        except Exception as e:
            print traceback.format_exc()

        return status
