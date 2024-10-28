from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship
from config.database import Base
from ...achievements.models import Achievement


class UserAchievement(Base):
    __tablename__ = "users_achievements"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    achievement: Mapped['Achievement'] = relationship('Achievement')
