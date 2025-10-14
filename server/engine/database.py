#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from server.base import Base, base_model
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        EDMS_MYSQL_DB = getenv('EDMS_MYSQL_DB')
        EDMS_ENV = getenv('EDMS_ENV')
        self.__engine = create_engine('sqlite///{}'.
                                      format(EDMS_MYSQL_DB))
        if EDMS_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve objects from storage"""
        objs = self.__session.query(cls).filter_by(id=id).first()
        return objs

    def count(self, cls=None):
        """count the number of objects in storage """
        if cls is None:
            count = 0
            for clss in classes.values():
                count += self.__session.query(clss).count()
        else:
            count = self.__session.query(cls).count()
        return count