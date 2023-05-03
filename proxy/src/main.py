import uvicorn
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from proxy.src.exceptions import rate_limit_exceeded_handler
from proxy.src.ratelimiter import limiter
from proxy.src.config import BASE_DIR, CORS_URL
from proxy.src.service.router import router as service_router
from proxy.src.service.middlewares import validate_ip, validate_fingerprint

app = FastAPI()
origins = [
    CORS_URL,
    "http://localhost:3000",
    "localhost",
]

app.state.limiter = limiter
app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")
app.middleware("http")(validate_ip)
app.middleware("http")(validate_fingerprint)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
app.include_router(service_router)
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
