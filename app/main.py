from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.exception.request_validation_handler import request_validation_handler
from app.lifespan.lifespan import lifespan
from app.core.setting import setting


if setting.ENV == "Dev":
    app = FastAPI(lifespan=lifespan)
else:
    app = FastAPI()

# デフォルトのValidationErrorのレスポンスを変更
app.add_exception_handler(RequestValidationError, request_validation_handler)

# routerのinclude処理

# # superuserのinclude処理
# app.include_router(superuser_login.router)
# app.include_router(management.router)

