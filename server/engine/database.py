#!/usr/bin/python3
"""Simple DBStorage using SQLAlchemy.

This file provides a small wrapper used by the rest of the project. It defaults
to a local SQLite file for development when EDMS_MYSQL_DB is not provided. It
imports project models (e.g. Account) so SQLAlchemy metadata is registered and
created on reload().
"""

from os import getenv
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session as SASession

# Import Base and models so metadata is populated
from server.base import Base
# Import models that should be registered in metadata
from server.account import Account  # ensure the Account table exists


class DBStorage:
    """A minimal SQLAlchemy-backed storage class used by the app.

    Methods are intentionally small and synchronous; they mirror the small set
    of actions used by the codebase (new, save, delete, get, count, list).
    """

    def __init__(self):
        db_url = getenv("EDMS_MYSQL_DB") or "sqlite:///./edms.db"
        # support URLs like sqlite:///./edms.db or a full postgres/mysql URL
        self.__engine = create_engine(db_url, echo=False, future=True)
        self.__session_factory = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session: Optional[SASession] = None

    def reload(self):
        """Create tables and prepare a session factory."""
        Base.metadata.create_all(self.__engine)
        self.__session = self.__session_factory

    def new(self, obj):
        """Add obj to current session."""
        if self.__session is None:
            self.reload()
        self.__session.add(obj)

    def save(self):
        """Commit current session."""
        if self.__session is None:
            self.reload()
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from session if provided."""
        if obj is None:
            return
        if self.__session is None:
            self.reload()
        self.__session.delete(obj)
        self.__session.commit()

    def get(self, cls, id):
        """Return an instance of cls by primary key id or None."""
        if self.__session is None:
            self.reload()
        return self.__session.query(cls).filter_by(id=id).first()

    def count(self, cls=None):
        """Return count of objects. If cls is None, count rows for known models."""
        if self.__session is None:
            self.reload()
        if cls is None:
            # For now only Account is a registered model in this project.
            return self.__session.query(Account).count()
        return self.__session.query(cls).count()

    def close(self):
        """Remove the scoped session."""
        if self.__session is not None:
            self.__session.remove()
