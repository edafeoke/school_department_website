#!/usr/bin/python3

from models.base_model import BaseModel, Base
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE') or 'file'


class Lecturer(User, BaseModel, Base):
    '''Lecturer class'''

    __tablename__ = 'lecturers'

    if HBNB_TYPE_STORAGE == 'db':
        title = Column(String(128), nullable=True)
        bio = Column(String(128), nullable=True)
        username = Column(String(128), nullable=False)
        role = Column(String(128), nullable=False)

        # roles = relationship('Role', backref='lecturer', cascade='delete')

    def __init__(self, *args, **kwargs):
        #     """initializes lecturer"""
        self.title = ''
        self.bio = ''
        self.username = ''
        self.role = 'lecturer'

        super().__init__(*args, **kwargs)
