from enum import Enum
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from config.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    users = relationship('User', secondary='users_achievements', back_populates='achievement')