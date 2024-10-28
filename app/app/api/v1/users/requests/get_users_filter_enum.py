from enum import Enum


class FilterEnum(Enum):
    NONE = 'None'
    MAX_ACHIEVEMENTS = 'MaxAchievements'
    MAX_VALUE = 'MaxValue'
    MAX_DELTA_VALUE = 'MaxDeltaValue'
    MIN_DELTA_VALUE = 'MinDeltaValue'
    WEEK_STREAK = 'WeekStreak'