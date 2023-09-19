#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey, Column


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(string(60), nullable=False, ForeignKey("state_id"))
    
    def __init__(self, name, state_id):
        """Define init method."""
        self.name = name
        self.state_id = state_id
