from starlette.testclient import TestClient
from app.domain.achievements.models import Achievement
from app.domain.users.models import User, UserAchievement
from app.domain.users.models.user import LanguageEnum
from app.main import app

client = TestClient(app)


def test_create_achievement(setup_test_db, override_get_session):
    request = {
        "names": [{
            "id": LanguageEnum.RU.value,
            "value": "Тестовое название"
        }],
        "descriptions": [{
            "id": LanguageEnum.EN.value,
            "value": "Test description"
        }],
        "value": 10
    }

    response = client.post("/achievements", json=request)
    db = setup_test_db()
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()
    assert response.status_code == 200
    assert response.json().get("value") == 10


def test_get_achievements(setup_test_db, override_get_session):
    db = setup_test_db()
    db.query(Achievement).delete()
    first_achievement = Achievement(
        names={LanguageEnum.RU.value: 'Название'},
        descriptions={LanguageEnum.RU.value: 'Описание'},
        value=10
    )
    db.add(first_achievement)
    second_achievement = Achievement(
        names={LanguageEnum.EN.value: 'Name'},
        descriptions={LanguageEnum.RU.value: 'Description'},
        value=20
    )
    db.add(second_achievement)
    db.commit()
    db.refresh(first_achievement)
    db.refresh(second_achievement)

    response = client.get("/achievements?offset=1&limit=1")
    db.query(Achievement).delete()
    db.close()
    assert response.status_code == 200
    assert len(response.json()) == 1
    response_data = response.json()
    assert response_data[0].get("value") == 20
