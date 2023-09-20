#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.place import Place


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(string(60), nullable=False, ForeignKey("state.id"))
    places = relationship("Place",
                          backref="cities",
                          cascade="all, delete-orphan",
                          passive_deletes=True)

    def __init__(self, *args, **kwargs):
        """Define init method."""
        super().__init__()
