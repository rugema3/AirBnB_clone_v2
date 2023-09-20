#!/usr/bin/python3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
rom sqlalchemy.ext.declarative import declarative_base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBConfig:
    """Database configuration class"""
    def __init__(self):
        self.user = os.getenv("HBNB_MYSQL_USER")
        self.password = os.getenv("HBNB_MYSQL_PWD")
        self.host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        self.database = os.getenv("HBNB_MYSQL_DB")
        self.env = os.getenv("HBNB_ENV")

class DBStorage:
    """DBStorage class for managing the database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        config = DBConfig()

        # Create the database engine
        self.__engine = create_engine(
            f'mysql+mysqldb://{config.user}:{config.password}@{config.host}:'
            '3306/{config.database}', pool_pre_ping=True)

        # Drop all tables if in test mode
        if config.env == "test":
            Base.metadata.drop_all(self.__engine)

        if config.env != "test":
            Base.metadata.create_all(self.__engine)

        # Create a new scoped session
        self.__session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))

    def all(self, cls=None):
        """Query all objects depending on the class name"""
        from models import classes

        objects = {}
        if cls:
            if type(cls) == str:
                cls = classes[cls]
            query_result = self.__session.query(cls).all()
        else:
            query_result = []
            for c in classes.values():
                query_result.extend(self.__session.query(c).all())

        for obj in query_result:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            objects[key] = obj
        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a new session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))

    def close(self):
        """Remove the session and close the connection"""
        self.__session.remove()
