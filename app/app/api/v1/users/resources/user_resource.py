from pydantic import BaseModel, Field
from app.domain.users.models.user import LanguageEnum


class UserResource(BaseModel):
    id: int = Field(
        examples=[1],
        description='ID пользователя'
    )
    name: str = Field(
        examples=["Сергей"],
        description='Имя пользователя'
    )
    lang: LanguageEnum = Field(
        examples=[LanguageEnum.EN],
        description='Выбранный язык системы'
    )
    value: int = Field(
        examples=[1],
        description='Суммарное число баллов'
    )
