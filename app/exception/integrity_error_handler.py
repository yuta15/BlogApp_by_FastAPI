from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.main import app


@app.exception_handler(IntegrityError)
async def integirity_error_handler(request, exc: IntegrityError):
    """
    IntegrityErrorが発生した際に発砲するError Handler
    status_code: 409
    """
    return JSONResponse(
        status_code=409,
        content={'detail': 'Conflict input data. Please check your params'}
    )