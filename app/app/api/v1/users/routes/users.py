from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.api.v1.users.requests.get_users_filter_enum import FilterEnum
from app.api.v1.users.resources.user_achievement_resource import UserAchievementResource
from app.api.v1.users.resources.user_resource import UserResource
from app.domain.users.actions.add_achievement_to_user_action import AddAchievementToUserAction
from app.domain.users.actions.get_user_achievements_action import GetUserAchievementsAction
from app.domain.users.actions.get_user_action import GetUserAction
from app.domain.users.actions.get_users_action import GetUsersAction

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get(
    "",
    description='Метод получения пользователя',
    summary='Метод получения пользователя',
    response_model=list[UserResource]
)
def get_users(
        filter: Optional[FilterEnum] = Query(
            description='Фильтр пользователей',
            default=FilterEnum.NONE,
        ),
        offset: int = Query(
            examples=[0],
            description='Смещение при пагинации',
            default=0
        ),
        limit: int = Query(
            examples=[10],
            description='Число получаемых записей',
            default=10
        ),
        action: GetUsersAction = Depends()
):
    return action.execute(filter, offset, limit)

@router.get(
    "/{user_id}",
    description='Метод получения пользователя',
    summary='Метод получения пользователя',
    response_model=UserResource
)
def get_user(user_id: int, action: GetUserAction = Depends()):
    return action.execute(user_id)

@router.get(
    "/{user_id}/achievements",
    description='Метод получения достижений пользователя',
    summary='Метод получения достижений пользователя',
    response_model=list[UserAchievementResource]
)
def get_user_achievements(
        user_id: int,
        action: GetUserAchievementsAction = Depends()
):
    return action.execute(user_id)

@router.post(
    "/{user_id}/achievements/{achievement_id}",
    description='Метод выдачи пользователю достижения',
    summary='Метод выдачи пользователю достижения'
)
def add_achievement_to_user(
        user_id: int,
        achievement_id: int,
        action: AddAchievementToUserAction = Depends()
):
    action.execute(user_id, achievement_id)
