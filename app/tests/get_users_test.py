from datetime import datetime, timedelta
from starlette.testclient import TestClient
from app.api.v1.users.requests.get_users_filter_enum import FilterEnum
from app.domain.achievements.models import Achievement
from app.domain.users.models import User, UserAchievement
from app.domain.users.models.user import LanguageEnum
from app.main import app

client = TestClient(app)


def test_get_users(setup_test_db, override_get_session):
    response = client.get("/users")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 0

def test_get_users_filter_is_none(setup_test_db, override_get_session):
    db = setup_test_db()
    first_user = User(
        name='Первый',
        lang=LanguageEnum.RU,
    )
    db.add(first_user)
    second_user = User(
        name='Второй',
        lang=LanguageEnum.EN,
    )
    db.add(second_user)
    db.commit()
    db.refresh(first_user)
    db.refresh(second_user)

    second_user_id = second_user.id

    query_params = {
        "filter": FilterEnum.NONE.value,
        "offset": 1,
        "limit": 1,
    }

    response = client.get("/users", params=query_params)
    db.query(User).delete()
    db.close()

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0].get("id") == second_user_id

def test_get_users_filter_is_max_achievements(setup_test_db, override_get_session):
    db = setup_test_db()
    first_user = User(
        name='Первый',
        lang=LanguageEnum.RU,
    )
    db.add(first_user)
    second_user = User(
        name='Второй',
        lang=LanguageEnum.EN,
    )
    db.add(second_user)
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
    db.refresh(first_user)
    db.refresh(second_user)
    db.refresh(first_achievement)
    db.refresh(second_achievement)

    f_user_f_achievement = UserAchievement(user_id=first_user.id, achievement_id=first_achievement.id)
    f_user_s_achievement = UserAchievement(user_id=first_user.id, achievement_id=second_achievement.id)
    s_user_f_achievement = UserAchievement(user_id=second_user.id, achievement_id=first_achievement.id)
    db.add(f_user_f_achievement)
    db.add(f_user_s_achievement)
    db.add(s_user_f_achievement)
    db.commit()

    first_user_id = first_user.id

    query_params = {
        "filter": FilterEnum.MAX_ACHIEVEMENTS.value,
    }

    response = client.get("/users", params=query_params)
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0].get("id") == first_user_id

def test_get_users_filter_is_max_value(setup_test_db, override_get_session):
    db = setup_test_db()
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()
    first_user = User(
        name='Третий',
        lang=LanguageEnum.RU,
    )
    db.add(first_user)
    second_user = User(
        name='Четвертый',
        lang=LanguageEnum.EN,
    )
    db.add(second_user)
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
    db.refresh(first_user)
    db.refresh(second_user)
    db.refresh(first_achievement)
    db.refresh(second_achievement)

    f_user_f_achievement = UserAchievement(user_id=first_user.id, achievement_id=first_achievement.id)
    f_user_s_achievement = UserAchievement(user_id=first_user.id, achievement_id=second_achievement.id)
    s_user_f_achievement = UserAchievement(user_id=second_user.id, achievement_id=first_achievement.id)
    db.add(f_user_f_achievement)
    db.add(f_user_s_achievement)
    db.add(s_user_f_achievement)
    db.commit()

    first_user_id = first_user.id

    query_params = {
        "filter": FilterEnum.MAX_VALUE.value,
    }

    response = client.get("/users", params=query_params)
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0].get("id") == first_user_id
    assert response_data[0].get("value") == 30

def test_get_users_filter_is_max_delta_value(setup_test_db, override_get_session):
    db = setup_test_db()
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()
    first_user = User(
        name='Пятый',
        lang=LanguageEnum.RU,
    )
    db.add(first_user)
    second_user = User(
        name='Шестой',
        lang=LanguageEnum.EN,
    )
    db.add(second_user)
    third_user = User(
        name='Седьмой',
        lang=LanguageEnum.EN,
    )
    db.add(third_user)
    first_achievement = Achievement(
        names={LanguageEnum.RU.value: 'Название'},
        descriptions={LanguageEnum.RU.value: 'Описание'},
        value=10
    )
    db.add(first_achievement)
    second_achievement = Achievement(
        names={LanguageEnum.EN.value: 'Name'},
        descriptions={LanguageEnum.RU.value: 'Description'},
        value=30
    )
    db.add(second_achievement)
    db.commit()
    db.refresh(first_user)
    db.refresh(second_user)
    db.refresh(first_achievement)
    db.refresh(second_achievement)

    f_user_f_achievement = UserAchievement(user_id=first_user.id, achievement_id=first_achievement.id)
    f_user_s_achievement = UserAchievement(user_id=first_user.id, achievement_id=second_achievement.id)
    s_user_s_achievement = UserAchievement(user_id=second_user.id, achievement_id=second_achievement.id)
    t_user_f_achievement = UserAchievement(user_id=third_user.id, achievement_id=first_achievement.id)
    db.add(f_user_f_achievement)
    db.add(f_user_s_achievement)
    db.add(s_user_s_achievement)
    db.add(t_user_f_achievement)
    db.commit()

    first_user_id = first_user.id
    third_user_id = third_user.id

    query_params = {
        "filter": FilterEnum.MAX_DELTA_VALUE.value,
    }

    response = client.get("/users", params=query_params)
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0].get("id") == first_user_id
    assert response_data[0].get("value") == 40
    assert response_data[1].get("id") == third_user_id
    assert response_data[1].get("value") == 10

def test_get_users_filter_is_min_delta_value(setup_test_db, override_get_session):
    db = setup_test_db()
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()
    first_user = User(
        name='Восьмой',
        lang=LanguageEnum.RU,
    )
    db.add(first_user)
    second_user = User(
        name='Девятый',
        lang=LanguageEnum.EN,
    )
    db.add(second_user)
    third_user = User(
        name='Десятый',
        lang=LanguageEnum.EN,
    )
    db.add(third_user)
    first_achievement = Achievement(
        names={LanguageEnum.RU.value: 'Название'},
        descriptions={LanguageEnum.RU.value: 'Описание'},
        value=10
    )
    db.add(first_achievement)
    second_achievement = Achievement(
        names={LanguageEnum.EN.value: 'Name'},
        descriptions={LanguageEnum.RU.value: 'Description'},
        value=30
    )
    db.add(second_achievement)
    db.commit()
    db.refresh(first_user)
    db.refresh(second_user)
    db.refresh(first_achievement)
    db.refresh(second_achievement)

    f_user_f_achievement = UserAchievement(user_id=first_user.id, achievement_id=first_achievement.id)
    f_user_s_achievement = UserAchievement(user_id=first_user.id, achievement_id=second_achievement.id)
    s_user_s_achievement = UserAchievement(user_id=second_user.id, achievement_id=second_achievement.id)
    t_user_f_achievement = UserAchievement(user_id=third_user.id, achievement_id=first_achievement.id)
    db.add(f_user_f_achievement)
    db.add(f_user_s_achievement)
    db.add(s_user_s_achievement)
    db.add(t_user_f_achievement)
    db.commit()

    first_user_id = first_user.id
    second_user_id = second_user.id

    query_params = {
        "filter": FilterEnum.MIN_DELTA_VALUE.value,
    }

    response = client.get("/users", params=query_params)
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0].get("id") == first_user_id
    assert response_data[0].get("value") == 40
    assert response_data[1].get("id") == second_user_id
    assert response_data[1].get("value") == 30

def test_get_users_filter_is_week_streak(setup_test_db, override_get_session):
    db = setup_test_db()
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()
    first_user = User(
        name='Восьмой',
        lang=LanguageEnum.RU,
    )
    db.add(first_user)
    second_user = User(
        name='Девятый',
        lang=LanguageEnum.EN,
    )
    db.add(second_user)
    db.commit()
    db.refresh(first_user)
    db.refresh(second_user)

    start_date = datetime.now()
    records = []

    for i in range(7):
        # Создаем запись с датой, увеличенной на i дней
        achievement = Achievement(
            names={LanguageEnum.RU.value: 'Название'},
            descriptions={LanguageEnum.RU.value: 'Описание'},
            value=10
        )
        db.add(achievement)
        db.commit()
        db.refresh(achievement)
        record_date = start_date + timedelta(days=i)
        user_achievement = UserAchievement(user_id=first_user.id, achievement_id=achievement.id, created_at=record_date)
        db.add(user_achievement)
        db.commit()

    first_user_id = first_user.id

    query_params = {
        "filter": FilterEnum.WEEK_STREAK.value,
    }

    response = client.get("/users", params=query_params)
    db.query(UserAchievement).delete()
    db.query(User).delete()
    db.query(Achievement).delete()
    db.close()

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0].get("id") == first_user_id
