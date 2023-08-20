#!/usr/bin/python3

from models.base_model import BaseModel, Base
from flask_login import UserMixin
from os import getenv
from werkzeug.security import generate_password_hash
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE') or 'file'


class User(BaseModel, Base, UserMixin):
    '''User class'''

    __abstract__ = True

    if HBNB_TYPE_STORAGE == 'db':
        username = Column(String(128), nullable=True)
        email = Column(String(128), nullable=True)
        password = Column(String(128), nullable=False)
        name = Column(String(128), nullable=True)
        session_id = Column(String(128), nullable=True)
        reset_token = Column(String(128), nullable=True)
        role = Column(String(128), nullable=False)


    def __init__(self, *args, **kwargs):
    #     """initializes user"""
        self.email = ''
        self.password = ''
        self.name = ''
        self.session_id = ''
        self.reset_token = ''
        self.role = ''
        self.username = ''
        super().__init__(self, *args, **kwargs)
    
    def hash_password(self, password):
        self.password = generate_password_hash(password)
