#!/usr/bin/python3

from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE') or 'file'


class Lecturer(BaseModel, Base):
    '''Lecturer class'''

    __tablename__ = 'lecturers'

    if HBNB_TYPE_STORAGE == 'db':
        title = Column(String(128), nullable=True)
        bio = Column(String(128), nullable=True)

        # roles = relationship('Role', backref='lecturer', cascade='delete')

    def __init__(self, *args, **kwargs):
        #     """initializes lecturer"""
        self.title = ''
        self.bio = ''

        super().__init__(*args, **kwargs)
