from typing import Dict

from sqlalchemy import Column, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.users.models.user import LanguageEnum
from config.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    names: Mapped[Dict[LanguageEnum, str]] = mapped_column(JSON, nullable=False)
    value = Column(Integer, nullable=False)
    descriptions: Mapped[Dict[LanguageEnum, str]] = mapped_column(JSON, nullable=False)
