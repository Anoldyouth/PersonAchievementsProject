from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import relationship

from config.database import Base


class LanguageEnum(Enum):
    RU = "ru"
    EN = "en"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lang = Column(SqlEnum(LanguageEnum), nullable=False)

    achievements = relationship('Achievement', secondary='users_achievements', back_populates=__tablename__)
