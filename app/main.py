from fastapi import FastAPI

from api import user, login, article
from core.db import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(article.router)