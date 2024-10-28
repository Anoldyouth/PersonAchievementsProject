from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.api.v1.achievements.requests.create_achievement_request import CreateAchievementRequest
from app.api.v1.achievements.resources.achievement_resource import AchievementResource
from app.api.v1.users.resources.user_resource import UserResource
from app.domain.achievements.actions.create_achievement_action import CreateAchievementAction
from app.domain.achievements.actions.get_achievements_action import GetAchievementsAction
from app.domain.users.actions.get_user_action import GetUserAction

router = APIRouter(
    prefix='/achievements',
    tags=['achievements']
)

@router.get(
    '',
    description='Метод получения достижений',
    summary='Метод получения достижений',
    response_model=list[AchievementResource]
)
def get_achievements(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, le=100),
        action: GetAchievementsAction = Depends()
):
    return action.execute(offset, limit)

@router.post(
    '',
    description='Метод создания достижения',
    summary='Метод создания достижения',
    response_model=AchievementResource
)
def create_achievement(
        request: CreateAchievementRequest,
        action: CreateAchievementAction = Depends()
):
    return action.execute(request)
