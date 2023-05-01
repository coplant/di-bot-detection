import sys

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from service.middlewares import validate_ip

sys.path.append("..")

from config import BASE_DIR
from service.router import router as service_router

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")
app.include_router(service_router)
app.middleware("http")(validate_ip)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
