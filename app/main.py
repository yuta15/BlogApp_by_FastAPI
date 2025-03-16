from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.exception.request_validation_handler import request_validation_handler
from app.lifespan.lifespan import lifespan
from app.core.setting import setting
from app.api.mode_checker import checker
from app.api.article import article


if setting.ENV == "Dev":
    app = FastAPI(lifespan=lifespan)
else:
    app = FastAPI()

# デフォルトのValidationErrorのレスポンスを変更
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.include_router(checker)
app.include_router(article)