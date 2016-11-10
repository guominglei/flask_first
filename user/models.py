# -*- coding:utf-8 -*-

"""
    用户模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
#from database import Base, db_session
from ..flask_sql_database import Base, db_session, db
import traceback


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    age = Column(Integer, default=20)
    password = Column(String(20), default="123456")
    admin = Column(Boolean, default=False)
    salary = Column(Float, default=1000.50)

    def __init__(self, name, age, password, admin=False, salary=None):
        self.name = name
        self.age = age
        self.password = password
        self.admin = admin
        self.salary = salary

    def __repr__(self):
        return "<User {}>".format(self.id)

    def __str__(self):
        return self.name

    def format(self):

        info = {
            "name":self.name,
            "age":self.age,
            "admin":self.admin,
            "salary":self.salary
        }

        return info

    @classmethod
    def get_list(cls, format=False):

        #items = cls.query.all()
        items = db_session().using_bind("slave").query(cls).all()

        if format:
            items = [item.format() for item in items]
        return items

    @classmethod
    def new_item(cls, name, age, password, salary, admin=False):

        name = name.strip()

        item = cls(name,
                   age,
                   password,
                   admin=admin,
                   salary=salary)

        db_session.add(item)
        db_session.commit()

    @classmethod
    def delete_item(cls, user_id):

        status = False
        try:
            item = cls.query.get(user_id)
            db_session.delete(item)
            db_session.commit()
            status = True
        except Exception, e:
            print traceback.format_exc()

        return status

    @classmethod
    def update_item(cls, user_id, name=None, age=None, salary=None):

        status = False
        try:
            item = cls.query.get(user_id)
            if name:
                item.name = name
            if age:
                item.age = age
            if salary:
                item.salary = salary
            db_session.add(item)
            db_session.commit()
            status = True
        except Exception,e:
            print traceback.format_exc()

        return status

