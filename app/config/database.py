from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic.v1 import BaseSettings


class DatabaseSettings(BaseSettings):
    database_host: str
    database_port: str
    database_user: str
    database_password: str
    database_db: str

    class Config:
        env_file = ".env"


settings = DatabaseSettings()

# Формирование строки подключения к базе данных
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_user}:{settings.database_password}@"
    f"{settings.database_host}:{settings.database_port}/{settings.database_db}"
)

# Настройка подключения через SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()
Base.metadata.create_all(bind=engine)


# Функция зависимости для получения сессии базы данных
def get_session():
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()

