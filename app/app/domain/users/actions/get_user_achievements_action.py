from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.users.resources.user_achievement_resource import UserAchievementResource
from app.domain.achievements.models import Achievement
from app.domain.users.models.user import User
from config.database import get_session

class GetUserAchievementsAction:
    def __init__(self, db: Session = Depends(get_session)):
        self.db = db

    def execute(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        result = []
        for user_achievement in user.achievements:
            achievement: Achievement = user_achievement.achievement
            name = achievement.names.get(user.lang.value)
            description = achievement.descriptions.get(user.lang.value)
            result.append(UserAchievementResource(
                id=achievement.id,
                name=name,
                description=description,
                value=achievement.value,
                created_at=user_achievement.created_at,
            ))

        return sorted(result, key=lambda x: x.created_at, reverse=True)
