from marshmallow import Schema, fields, ValidationError, validate, post_load, INCLUDE, EXCLUDE
from datetime import datetime
from crypt import Crypt
from helpers import TrimmedString


class User(object):
    __slots__ = ('_id', 'first_name', 'middle_name', 'last_name', 'password',
                 'phone', 'session_token', 'created_at', 'updated_at')

    def __init__(self, _id=None, first_name=None, middle_name=None, last_name=None, password=None, phone=None, session_token=None, created_at=None, updated_at=None):
        if _id:
            self._id = _id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        if password:
            self.password = Crypt().encrypt(password)
        self.phone = phone
        self.session_token = session_token
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return 'name=' + str(self.first_name) + str(self.last_name)

    def to_json(self):
        return self.__slotted_to_dict()

    def __slotted_to_dict(self):
        return {s: getattr(self, s) for s in self.__slots__ if hasattr(self, s)}


class UserSchema(Schema):
    first_name = TrimmedString(required=True, validate=validate.Length(min=2))
    middle_name = fields.String()
    last_name = fields.String(required=True)
    password = fields.String(required=True, validate=validate.Regexp(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$", error='Password is not strong enough'),error_messages={
          'required': 'Password is required on user creation',
          'invalid': 'Password is not strong enough',
            "validator_failed":'Password is not strong enough'
    })
    phone = TrimmedString(required=True, validate=validate.Regexp(r"(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}", error="Input does not seems like a phone number"))
    session_token = fields.String(required=True)

    class Meta():
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs):
        return User(**data)
