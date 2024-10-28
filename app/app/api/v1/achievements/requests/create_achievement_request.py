from pydantic import BaseModel, Field

from app.domain.users.models.user import LanguageEnum


class LangValue(BaseModel):
    id: LanguageEnum = Field(
        examples=[LanguageEnum.EN.value],
        description='Язык'
    )
    value: str = Field(
        examples=['Значение'],
        description='Значение поля'
    )


class CreateAchievementRequest(BaseModel):
    names: list[LangValue] = Field(
        description='Названия достижения для различных языков'
    )
    descriptions: list[LangValue] = Field(
        description='Описания достижения для различных языков'
    )
    value: int = Field(
        examples=[10],
        description='Число баллов'
    )