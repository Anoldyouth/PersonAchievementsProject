from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.v1.achievements.requests.create_achievement_request import CreateAchievementRequest
from app.api.v1.achievements.resources.achievement_resource import LangValueResource, AchievementResource
from app.domain.achievements.models import Achievement
from config.database import get_session


class CreateAchievementAction:
    def __init__(self, db: Session = Depends(get_session)):
        self.db = db

    def execute(self, request: CreateAchievementRequest):
        names = {name.id.value: name.value for name in request.names}
        descriptions = {description.id.value: description.value for description in request.descriptions}
        achievement = Achievement(
            names=names,
            descriptions=descriptions,
            value=request.value,
        )
        self.db.add(achievement)
        self.db.commit()
        self.db.refresh(achievement)

        return self.__map_achievement(achievement)

    def __map_achievement(self, achievement: Achievement):
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
