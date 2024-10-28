from starlette.testclient import TestClient
from app.domain.achievements.models import Achievement
from app.domain.users.models import User, UserAchievement
from app.domain.users.models.user import LanguageEnum
from app.main import app

client = TestClient(app)


def test_get_user_user_not_found(setup_test_db, override_get_session):
    response = client.get("/users/0")
    assert response.status_code == 404

def test_get_user_user_without_achievements(setup_test_db, override_get_session):
    db = setup_test_db()
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    user = User(name='test name', lang=LanguageEnum.RU)
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": user.id,
        "name": 'test name',
        "lang": LanguageEnum.RU.value,
        "value": 0
    }
    db.query(User).delete()
    db.close()

def test_get_user_user_with_achievements(setup_test_db, override_get_session):
    db = setup_test_db()
    user = User(name='test name', lang=LanguageEnum.RU)
    db.add(user)
    db.commit()
    db.refresh(user)
    achievement = Achievement(
        names={LanguageEnum.RU.value:'Название'},
        descriptions={LanguageEnum.RU.value:'Описание'},
        value=10
    )
    db.add(achievement)
    db.commit()
    db.refresh(achievement)
    user_achievement = UserAchievement(user_id=user.id, achievement_id=achievement.id)
    db.add(user_achievement)
    db.commit()

    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": user.id,
        "name": 'test name',
        "lang": LanguageEnum.RU.value,
        "value": 10
    }
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()

def test_get_user_achievements(setup_test_db, override_get_session):
    db = setup_test_db()
    user = User(name='test name', lang=LanguageEnum.RU)
    db.add(user)
    db.commit()
    db.refresh(user)
    first_achievement = Achievement(
        names={LanguageEnum.RU.value:'Название'},
        descriptions={LanguageEnum.RU.value:'Описание'},
        value=10
    )
    db.add(first_achievement)
    second_achievement = Achievement(
        names={LanguageEnum.EN.value: 'Name'},
        descriptions={LanguageEnum.EN.value: 'Description'},
        value=20
    )
    db.add(second_achievement)
    db.commit()
    db.refresh(first_achievement)
    db.refresh(second_achievement)
    first_user_achievement = UserAchievement(user_id=user.id, achievement_id=first_achievement.id)
    second_user_achievement = UserAchievement(user_id=user.id, achievement_id=second_achievement.id)
    db.add(first_user_achievement)
    db.add(second_user_achievement)
    db.commit()
    first_achievement_id = first_achievement.id
    second_achievement_id = second_achievement.id

    response = client.get(f"/users/{user.id}/achievements")
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0]["id"] == first_achievement_id
    assert response_data[0]["name"] == "Название"
    assert response_data[0]["description"] == "Описание"
    assert response_data[0]["value"] == 10
    assert response_data[1]["id"] == second_achievement_id
    assert response_data[1]["name"] == None
    assert response_data[1]["description"] == None
    assert response_data[1]["value"] == 20


def test_create_user_achievement_pair(setup_test_db, override_get_session):
    db = setup_test_db()
    user = User(name='test name', lang=LanguageEnum.RU)
    db.add(user)
    db.commit()
    db.refresh(user)
    achievement = Achievement(
        names={LanguageEnum.RU.value:'Название'},
        descriptions={LanguageEnum.RU.value:'Описание'},
        value=10
    )
    db.add(achievement)
    db.commit()
    db.refresh(achievement)

    response = client.post(f"/users/{user.id}/achievements/{achievement.id}")
    assert response.status_code == 200

    user_achievement = (db.query(UserAchievement)
                        .filter(UserAchievement.user_id == user.id and achievement.id == UserAchievement.achievement_id)
                        .first())

    assert user_achievement is not None
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()