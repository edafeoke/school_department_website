#!/usr/bin/python3

from models.base_model import BaseModel, Base
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE') or 'file'


class Student(User, BaseModel, Base):
    '''Student class'''

    __tablename__ = 'students'

    if HBNB_TYPE_STORAGE == 'db':
        mat_number = Column(String(128), nullable=True, unique=True)
        level = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        #     """initializes student"""
        self.role = 'student'
        self.mat_number = ''
        self.level = ''
        self.sex = ''
        super().__init__(self, *args, **kwargs)
