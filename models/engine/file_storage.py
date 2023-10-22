#!/usr/bin/python3
"""This module defines a class for file storage in AirBnB."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class FileStorage:
    """This class serializes instances to a JSON file and deserializes JSON
    file to instances.

    Attributes:
        __file_path (str): The path to the JSON file for storage.
        __objects (dict): A dictionary for storing objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Retrieve all or specific objects from the storage.

        Args:
            cls (class, optional): The class to filter objects.
            Defaults to None.

        Returns:
            dict: A dictionary containing the objects.
        """
        result_dict = {}
        if cls:
            storage_dict = self.__objects
            for key in storage_dict:
                key_parts = key.replace('.', ' ').split()
                if key_parts[0] == cls.__name__:
                    result_dict[key] = storage_dict[key]
            return result_dict
        else:
            return self.__objects

    def new(self, obj):
        """Add a new object to the storage.

        Args:
            obj (BaseModel): The object to add.
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Serialize the objects to the JSON file."""
        obj_dict = {}
        for key, value in self.__objects.items():
            obj_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserialize objects from the JSON file."""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as file:
                object_dict = json.load(file)
                for key, value in object_dict.items():
                    instance = eval(value["__class__"])(**value)
                    self.__objects[key] = instance
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete an existing object from storage.

        Args:
            obj (BaseModel, optional): The object to delete. Defaults to None.
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """Close the storage by calling reload()."""
        self.reload()
