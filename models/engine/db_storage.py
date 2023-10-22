#!/usr/bin/python3
"""Module for SQLAlchemy-based database storage"""
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class MyDBConfig:
    """Database configuration class for configuring the database connection"""
    def __init__(self):
        """
        Initialize a new MyDBConfig instance.

        This class is responsible for reading environmental variables
        to configure the connection to the database.

        Attributes:
            user (str): The database user.
            password (str): The database user's password.
            host (str): The database host.
            database (str): The name of the database.
            env (str): The environment (e.g., 'development' or 'test').
        """
        self.user = getenv("HBNB_MYSQL_USER")
        self.my_password = getenv("HBNB_MYSQL_PWD")
        self.host = getenv("HBNB_MYSQL_HOST", "localhost")
        self.db = getenv("HBNB_MYSQL_DB")
        self.env = getenv("HBNB_ENV")


class MyDBStorage:
    """Manage the database and data storage using SQLAlchemy"""
    __my_engine = None
    __my_session = None

    def __init__(self):
        """
        Initialize a new MyDBStorage instance.

        This class is responsible for managing the database and data storage
        using SQLAlchemy. It connects to the database, creates tables, and
        provides methods to query and manipulate data.

        If the environment is set to 'test', existing tables are dropped
        and new tables are created for testing purposes.
        """
        config = MyDBConfig()

        connection_string = 'mysql+mysqldb://{}:{}@{}'.format(
                config.user, config.my_password, config.host
                )
        self.__my_engine = create_engine(
                connection_string + '/{}'.format(config.db),
                pool_pre_ping=True
                )

        if config.env == "test":
            Base.metadata.drop_all(self.__my_engine)
            Base.metadata.create_all(self.__my_engine)

        sec = sessionmaker(bind=self.__my_engine, expire_on_commit=False)
        self.__my_session = scoped_session(sec)

    def all(self, cls=None):
        """
        Query and return objects from the database.

        This method allows querying objects from the database. If the 'cls'
        parameter is provided, it returns objects of the specified class. If
        'cls' is not provided, it returns all objects from all supported
        classes.

        Args:
            cls (str or class, optional): The class name as a string or the
                class itself. If provided, only objects of the specified class
                are returned.

        Returns:
            dict: A dictionary containing the queried objects with keys in the
                format '<class name>.<object id>'.
        """
        my_dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__my_session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                my_dic[key] = elem
        else:
            my_classes = [State, City, User, Place, Review, Amenity]
            for clase in my_classes:
                query = self.__my_session.query(clase)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    my_dic[key] = elem
        return my_dic

    def new(self, obj):
        """
        Add a new object to the current database session.

        This method adds a new object to the current database session,allowing
        it to be saved to the database during the next 'save' operation.

        Args:
            obj (BaseModel): The object to be added to the session.
        """
        self.__my_session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.

        This method saves all the changes made to the current database session,
        effectively writing the changes to the database.
        """
        self.__my_session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the current database session.

        This method deletes the provided object from the current
        database session.
        The object is not removed from the database but will not be
        saved during the next 'save' operation.

        Args:
            obj (BaseModel, optional): The object to be deleted from the
            session.
        """
        if obj:
            self.__my_session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and create a new session.

        This method is responsible for creating all the necessary tables in the
        database and creating a new session to manage the database operations.
        """
        Base.metadata.create_all(self.__my_engine)
        sec = sessionmaker(bind=self.__my_engine, expire_on_commit=False)
        self.__my_session = scoped_session(sec)

    def close(self):
        """
        Remove the session and close the connection to the database.

        This method removes the current session and closes the connection
        to the database, ensuring proper cleanup and resource management.
        """
        self.__my_session.close()
