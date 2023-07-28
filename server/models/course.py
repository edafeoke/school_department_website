#!/usr/bin/python3

from models.base_model import BaseModel, Base
from os import getenv
# import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE') or 'file'


class Course(BaseModel, Base):
    '''Course class'''

    __tablename__ = 'courses'

    if HBNB_TYPE_STORAGE == 'db':
        title = Column(String(256), nullable=False)
        lecturer_id = Column(String(256),  ForeignKey('lecturers.id'), nullable=False)
        code = Column(String(256), nullable=False)


    def __init__(self, *args, **kwargs):
    #     """initializes user"""
        self.lecturer_id = ''
        self.title = ''
        self.code = False
        super().__init__(*args, **kwargs)
