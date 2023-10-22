#!/usr/bin/python3
"""This module defines a class for file storage in AirBnB Clone."""

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
    """This class serializes instances to a JSON file and deserializes
    JSON file to instances.

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

        my_dict = {}
        if cls:
            my_dictionary = self.__objects
            for my_key in my_dictionary:
                my_partition = my_key.replace('.', ' ')
                my_partition = shlex.split(my_partition)
                if (my_partition[0] == cls.__name__):
                    my_dict[my_key] = self.__objects[my_key]
            return my_dict
        else:
            return self.__objects

    def new(self, obj):
        """Add a new object to the storage.

        Args:
            obj (BaseModel): The object to add.
        """

        if obj:
            my_key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[my_key] = obj

    def save(self):
        """Serialize the objects to the JSON file."""
        my_dict = {}
        for my_key, my_value in self.__objects.items():
            my_dict[my_key] = my_value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as my_f:
            json.dump(my_dict, my_f)

    def reload(self):
        """Deserialize objects from the JSON file."""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as my_f:
                for my_key, my_value in (json.load(my_f)).items():
                    my_value = eval(my_value["__class__"])(**my_value)
                    self.__objects[my_key] = my_value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete an existing object from storage.

        Args:
            obj (BaseModel, optional): The object to delete. Defaults to None.
        """

        if obj:
            my_key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[my_key]

    def close(self):
        """Close the storage by calling reload()."""
        self.reload()
