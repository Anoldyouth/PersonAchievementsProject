from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.users.resources.user_resource import UserResource
from app.domain.users.models.user import User
from config.database import get_session


class GetUserAction:
    def __init__(self, db: Session = Depends(get_session)):
        self.db = db

    def execute(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResource(
            id=user.id,
            name=user.name,
            lang=user.lang,
            value=user.get_total_value()
        )
