#!/usr/bin/python3
"""Account SQLAlchemy model for EDMS"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from server.base import Base


class Account(Base):
    """Represents a user account."""
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), default="staff", nullable=False)
    status = Column(String(32), default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

#!/usr/bin/python3

"""an account model for user"""
