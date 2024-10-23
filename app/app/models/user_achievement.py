from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from config.database import Base


class UserAchievement(Base):
    __tablename__ = "users_achievements"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="users")