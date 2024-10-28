import pytest
from alembic.command import upgrade
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from config.database import DatabaseSettings, Base, get_session
from utils import alembic_config_from_url


# Загружаем тестовые настройки
class TestDatabaseSettings(DatabaseSettings):
    class Config:
        env_file = ".env.testing"


settings = TestDatabaseSettings()

# Создаем строку подключения к тестовой базе данных
TEST_DATABASE_URL = (
    f"postgresql://{settings.database_user}:{settings.database_password}@"
    f"{settings.database_host}:{settings.database_port}/{settings.database_db}"
)

@pytest.fixture(scope='function')
def setup_test_db():
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)  # Создание всех таблиц

    # Применение миграций
    alembic_config = alembic_config_from_url(TEST_DATABASE_URL)
    upgrade(alembic_config, 'head')

    yield TestingSessionLocal
    Base.metadata.drop_all(bind=engine)  # Удаление всех таблиц после тестов

@pytest.fixture(scope="function")
def override_get_session(setup_test_db):
    def get_test_session():
        db = setup_test_db()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = get_test_session
    yield
    app.dependency_overrides.pop(get_session)
