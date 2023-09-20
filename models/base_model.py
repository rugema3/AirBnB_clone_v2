#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            # from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # storage.new(self)
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            # Delete the '__class__' key if it exists in kwargs.
            if '__class__' in kwargs:
                del kwargs['__class__']

            # Update the instance's attributes with the values from kwargs.
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}

        # Copy all attributes from the instance's __dict__ to the dictionary.
        dictionary.update(self.__dict__)

        # Remove the '_sa_instance_state' key if it exists in the dictionary.
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']

        # Add '__class__' key to the dictionary with the class name.
        class_name = str(type(self)).split('.')[-1]
        class_name = class_name.split('\'')[0]
        dictionary['__class__'] = class_name

        # Convert created_at and updated_at to ISO format.
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary

    def delete(self):
        """"Delete the current instance from the storage"""
        from models import storage

        # Use the storage's delete method to remove the instance
        storage.delete(self)
