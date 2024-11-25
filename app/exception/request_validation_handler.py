
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def request_validation_handler(request: Request, exc: RequestValidationError):
    """
    RequestValidationErrorの動作をオーバーライド。
    デフォルト:
        status_code: 422
        detail: AssertionError
    オーバーライド後:
        status_code: 400
        detail: Bad request
    """
    return JSONResponse(
        status_code=400, 
        content={"detail": 'Bad Request. Please Check your input data'},
        )