from fastapi import FastAPI

from app.api import user, login, article


app = FastAPI()
app.include_router(user.router)
app.include_router(login.router)
app.include_router(article.router)