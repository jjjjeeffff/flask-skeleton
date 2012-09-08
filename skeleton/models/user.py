# -*- coding: utf-8 -*-
"""
    skeleton.models.user
    ~~~~~~~~~~~~~~~~~~~~

    User and related UserMeta base objects. To be subclassed by separate user
    types. Basic functions are included for Flask-Login.

    :copyright: (c) 2012 by Jeff Long
"""


from .. import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    pwhash = db.Column(db.String(60))
    level = db.Column(db.Integer(1))

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __init__(self):
        pass

    def __repr__(self):
        return '<User %r>' % self.email


class UserMeta(db.Model):
    __tablename__ = 'user_meta'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(16))
    val = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref=db.backref('user_meta'))
