from datetime import timedelta

from fastapi import Depends
from sqlalchemy import func, literal_column
from sqlalchemy.orm import Session, aliased

from app.api.v1.users.requests.get_users_filter_enum import FilterEnum
from app.api.v1.users.resources.user_resource import UserResource
from app.domain.achievements.models import Achievement
from app.domain.users.models import User, UserAchievement
from config.database import get_session


class GetUsersAction:
    def __init__(self, db: Session = Depends(get_session)):
        self.db = db

    def execute(self, filter: FilterEnum, offset: int, limit: int):
        match filter:
            case FilterEnum.NONE: return self.__filter_is_none(offset, limit)
            case FilterEnum.MAX_ACHIEVEMENTS: return self.__filter_is_max_achievements()
            case FilterEnum.MAX_VALUE: return self.__filter_is_max_value()
            case FilterEnum.MAX_DELTA_VALUE: return self.__filter_is_max_delta_value()
            case FilterEnum.MIN_DELTA_VALUE: return self.__filter_is_min_delta_value()
            case FilterEnum.WEEK_STREAK: return self.__filter_is_week_streak()

    def __filter_is_none(self, offset: int, limit: int):
        users = self.db.query(User).order_by(User.id).offset(offset).limit(limit).all()

        return [UserResource(
            id=user.id,
            name=user.name,
            lang=user.lang,
            value=user.get_total_value()
        ) for user in users]

    '''
    Метод получения пользователей
    '''
    def __filter_is_none(self, offset: int, limit: int):
        users = self.db.query(User).order_by(User.id).offset(offset).limit(limit).all()

        return [UserResource(
            id=user.id,
            name=user.name,
            lang=user.lang,
            value=user.get_total_value()
        ) for user in users]

    '''
    Метод получения пользователя с максимальным числом достижений
    '''
    def __filter_is_max_achievements(self):
        subquery = (self.db.query(
            UserAchievement.user_id,
            func.count(UserAchievement.achievement_id).label("achievement_count")
        )
                    .group_by(UserAchievement.user_id)
                    .order_by(func.count(UserAchievement.achievement_id).desc())
                    .limit(1)
                    .subquery())
        user = self.db.query(User).join(subquery, User.id == subquery.c.user_id).first()

        return [UserResource(
            id=user.id,
            name=user.name,
            lang=user.lang,
            value=user.get_total_value()
        )]

    '''
    Метод получения пользователя с максимальным числом баллов
    '''
    def __filter_is_max_value(self):
        subquery = (self.db.query(
            UserAchievement.user_id,
            func.sum(Achievement.value).label("total_value")
        )
                    .join(Achievement, UserAchievement.achievement_id == Achievement.id)
                    .group_by(UserAchievement.user_id)
                    .order_by(func.sum(Achievement.value).desc())
                    .limit(1)
                    .subquery())
        user = self.db.query(User).join(subquery, User.id == subquery.c.user_id).first()

        return [UserResource(
            id=user.id,
            name=user.name,
            lang=user.lang,
            value=user.get_total_value()
        )]

    '''
    Метод получения пользователей с максимальной разницей в набранных баллах
    '''
    def __filter_is_max_delta_value(self):
        # Подзапрос для вычисления сумм очков для каждого пользователя
        user_points = (self.db.query(
            UserAchievement.user_id,
            func.sum(Achievement.value).label("total_points")
        )
                       .join(Achievement, UserAchievement.achievement_id == Achievement.id)
                       .group_by(UserAchievement.user_id)
                       .subquery())

        # Получаем максимальное и минимальное значения из user_points
        max_points = self.db.query(
            func.max(user_points.c.total_points).label("max_points")
        ).scalar()

        min_points = self.db.query(
            func.min(user_points.c.total_points).label("min_points")
        ).scalar()

        # Запрос на получение пользователей с максимальными и минимальными очками
        users_max = self.db.query(User).join(user_points, User.id == user_points.c.user_id) \
            .filter(user_points.c.total_points == max_points).all()
        users_min = self.db.query(User).join(user_points, User.id == user_points.c.user_id) \
            .filter(user_points.c.total_points == min_points).all()

        result_users = []

        # Обработка пользователей с максимальными очками
        for user in users_max:
            result_users.append(UserResource(
                id=user.id,
                name=user.name,
                lang=user.lang,
                value=user.get_total_value()
            ))

        # Обработка пользователей с минимальными очками
        for user in users_min:
            result_users.append(UserResource(
                id=user.id,
                name=user.name,
                lang=user.lang,
                value=user.get_total_value()
            ))

        return result_users

    '''
    Метод получения пользователей с минимальной разницей в набранных баллах
    '''

    def __filter_is_min_delta_value(self):
        # Подзапрос для вычисления сумм очков для каждого пользователя
        user_points = (
            self.db.query(
                UserAchievement.user_id,
                func.sum(Achievement.value).label("total_points")
            )
            .join(Achievement, UserAchievement.achievement_id == Achievement.id)
            .group_by(UserAchievement.user_id)
            .subquery()
        )

        # Создаем алиасы для подзапроса, чтобы найти пары пользователей
        u1 = aliased(user_points)
        u2 = aliased(user_points)

        # Находим минимальную разницу между очками любых двух пользователей
        min_delta = (self.db.query(
            u1.c.user_id.label("user_1_id"),
            u2.c.user_id.label("user_2_id"),
            func.abs(u1.c.total_points - u2.c.total_points).label(
                "points_diff"
            ),
        )
         .filter(u1.c.user_id < u2.c.user_id)
         .order_by(literal_column("points_diff").asc())
         .first())

        users = [
            self.db.query(User).filter(min_delta.user_1_id == User.id).first(),
            self.db.query(User).filter(min_delta.user_2_id == User.id).first(),
        ]

        result_users = [
            UserResource(
                id=user.id,
                name=user.name,
                lang=user.lang,
                value=user.get_total_value()
            )
            for user in users
        ]

        return result_users

    '''
    Метод получения пользователей с достижениями, полученными 7 дней подряд
    '''
    def __filter_is_week_streak(self):
        # Получаем все уникальные даты получения достижений для каждого пользователя
        user_dates = (
            self.db.query(
                UserAchievement.user_id,
                UserAchievement.created_at
            )
            .distinct()
            .order_by(UserAchievement.user_id, UserAchievement.created_at)
            .subquery()
        )

        # Получаем всех пользователей
        users_with_week_streak = []

        # Группируем по пользователям
        user_ids = self.db.query(user_dates.c.user_id).distinct().all()

        for user_id, in user_ids:
            # Получаем все уникальные даты для данного пользователя
            dates = self.db.query(user_dates.c.created_at).filter(user_dates.c.user_id == user_id).all()
            unique_dates = [date[0] for date in dates]  # Преобразуем к обычному списку

            # Проверяем наличие 7 последовательных дней
            for i in range(len(unique_dates) - 6):  # Чтобы не выйти за пределы
                if unique_dates[i + 6].date() - unique_dates[i].date() == timedelta(days=6):
                    users_with_week_streak.append(user_id)
                    break  # Достаточно одного совпадения

        # Получаем пользователей по найденным идентификаторам
        users = self.db.query(User).filter(User.id.in_(users_with_week_streak)).all()

        # Формируем результат
        return [UserResource(
            id=user.id,
            name=user.name,
            lang=user.lang,
            value=user.get_total_value()
        ) for user in users]