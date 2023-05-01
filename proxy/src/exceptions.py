from slowapi.errors import RateLimitExceeded
from starlette import status
from starlette.requests import Request
from starlette.responses import Response


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    response = Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content="Too many requests")
    return response
