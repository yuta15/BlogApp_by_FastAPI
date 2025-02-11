from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.main import app


@app.exception_handler(OperationalError)
async def operational_error_handler(request, exc: OperationalError):
    """
    OperationalErrorが発生した際に発砲するError Handler
    status_code: 500
    """
    return JSONResponse(
        status_code=500, 
        content={'detail': 'Internal Server Error. Please try again later.'}
        )