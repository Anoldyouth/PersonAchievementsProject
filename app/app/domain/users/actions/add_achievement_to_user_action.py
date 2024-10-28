from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.achievements.models import Achievement
from app.domain.users.models import UserAchievement
from app.domain.users.models.user import User
from config.database import get_session


class AddAchievementToUserAction:
    def __init__(self, db: Session = Depends(get_session)):
        self.db = db

    def execute(self, user_id: int, achievement_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        achievement = self.db.query(Achievement).filter(Achievement.id == achievement_id).first()
        if achievement is None:
            raise HTTPException(status_code=404, detail="Achievement not found")

        user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement_id)
        self.db.add(user_achievement)
        self.db.commit()
        self.db.refresh(user_achievement)
