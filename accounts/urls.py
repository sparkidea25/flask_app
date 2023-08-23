from sqlalchemy import inspect
from datetime import datetime
from flask_validator import ValidateEmail, ValidateString, ValidateCountry
from sqlalchemy.orm import validates

from .. import db # from __init__.py

class Account(db.Model):
    id           = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    created      = db.Column(db.DateTime(timezone=True), default=datetime.now)                           # The Date of the Instance Creation => Created one Time when Instantiation
    updated      = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)    # The Date of the Instance Update => Changed with Every Update

    # user input
    email = db.Column(db.String(100), nullable=false, unique=True)
    username = db.Column(db.String(100), nullable=false)
    dob = db.Column(db.Date)
    country = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))

    @classmethod
    def __declare__last__(cls):
        ValidateEmail(Account.email, True, True, "The email is not valid. Please check it") # True => Allow internationalized addresses, True => Check domain name resolution.)
        ValidateString(Account.username, True, True, "The username type must be string")
        ValidateCountry(Account.country, True, True, "The country is not valid")

    @validates('username')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '': return None
        else: return value

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return "<%r>" % self.email