#!/usr/bin/python3

from email.policy import default
from models.base_model import BaseModel, Base
from os import getenv
# import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE') or 'file'


class News(BaseModel, Base):
    '''News class'''

    __tablename__ = 'news'

    if HBNB_TYPE_STORAGE == 'db':
        title = Column(String(256), nullable=False)
        content = Column(String(1024), nullable=False)
        # user_id = Column(String(256),  ForeignKey('users.id'), nullable=False)


    def __init__(self, *args, **kwargs):
    #     """initializes news"""
        # self.user_id = ''
        self.title = ''
        self.content = ""
        super().__init__(*args, **kwargs)
