from fastapi import FastAPI

from app.api.v1.achievements.routes import achievements
from app.api.v1.users.routes import users

app = FastAPI()

app.include_router(users.router)
app.include_router(achievements.router)