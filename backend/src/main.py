from fastapi import FastAPI

from src.home.router import router as home_router

app = FastAPI()
app.include_router(home_router)
