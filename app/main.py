from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.user import general_user, login, article
from app.api.superuser import management, superuser_login
from app.exception.request_validation_handler import request_validation_handler

app = FastAPI()

# デフォルトのValidationErrorのレスポンスを変更
app.add_exception_handler(RequestValidationError, request_validation_handler)

# routerのinclude処理
app.include_router(general_user.router)
app.include_router(login.router)
app.include_router(article.router)

# superuserのinclude処理
app.include_router(superuser_login.router)
app.include_router(management.router)