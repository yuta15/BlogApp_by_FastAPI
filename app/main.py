from fastapi import FastAPI

from api import user, login
from core.db import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(login.router)