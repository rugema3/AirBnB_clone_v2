#!/usr/bin/python3
"""This is the state class"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: state name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        storage_data = models.storage.all()
        city_list = []
        result = []
        for key in storage_data:
            city_info = key.replace('.', ' ')
            city_info = shlex.split(city)
            if (city[0] == 'City'):
                city_list.append(storage_data[key])
        for city_elem in city_list:
            if (city_elem.state_id == self.id):
                result.append(city_elem)
        return (result)
