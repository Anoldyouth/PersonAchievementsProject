from pydantic import BaseModel, Field

from app.domain.users.models.user import LanguageEnum


class LangValueResource(BaseModel):
    id: LanguageEnum = Field(
        examples=[LanguageEnum.EN.value],
        description='Язык'
    )
    value: str = Field(
        examples=['Значение'],
        description='Значение поля'
    )


class AchievementResource(BaseModel):
    id: int = Field(
        examples=[1],
        description='ID достижения'
    )
    names: list[LangValueResource] = Field(
        description='Названия достижения для различных языков'
    )
    descriptions: list[LangValueResource] = Field(
        description='Описания достижения для различных языков'
    )
    value: int = Field(
        examples=[10],
        description='Число баллов'
    )
