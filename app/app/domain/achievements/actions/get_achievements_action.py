from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.v1.achievements.resources.achievement_resource import LangValueResource, AchievementResource
from app.domain.achievements.models import Achievement
from config.database import get_session


class GetAchievementsAction:
    def __init__(self, db: Session = Depends(get_session)):
        self.db = db

    def execute(self, offset: int, limit: int):
        achievements = (self.db.query(Achievement)
                        .order_by(Achievement.id)
                        .offset(offset)
                        .limit(limit)
                        .all())
        result = []
        for achievement in achievements:
            result.append(self.__map_achievement(achievement))

        return result

    def __map_achievement(self, achievement: Type[Achievement]):
        descriptions = []
        for lang, value in achievement.descriptions.items():
            descriptions.append(LangValueResource(id=lang, value=value))
        names = []
        for lang, value in achievement.names.items():
            names.append(LangValueResource(id=lang, value=value))

        return AchievementResource(
            id=achievement.id,
            descriptions=descriptions,
            names=names,
            value=achievement.value
        )