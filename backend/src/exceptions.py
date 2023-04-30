from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
