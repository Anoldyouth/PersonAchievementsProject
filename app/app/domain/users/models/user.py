from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, func
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING
from config.database import Base

if TYPE_CHECKING:
    from .user_achievement import UserAchievement

class LanguageEnum(Enum):
    RU = "ru"
    EN = "en"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lang: LanguageEnum = Column(SqlEnum(LanguageEnum), nullable=False)

    achievements: Mapped[list['UserAchievement']] = relationship('UserAchievement')

    def get_total_value(self):
        return sum(achievement.achievement.value for achievement in self.achievements)
