from fastapi import FastAPI

from api import user
from core.db import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)