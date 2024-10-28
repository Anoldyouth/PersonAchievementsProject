from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserAchievementResource(BaseModel):
    id: int = Field(
        examples=[1],
        description='ID достижения'
    )
    name: Optional[str] = Field(
        description='Название достижения на языке пользователя',
    )
    description: Optional[str] = Field(
        description='Описание достижения на языке пользователя'
    )
    value: int = Field(
        examples=[10],
        description='Число баллов'
    )
    created_at: datetime = Field(
        examples=[datetime(2024, 10, 27)],
        description='Дата получения'
    )
