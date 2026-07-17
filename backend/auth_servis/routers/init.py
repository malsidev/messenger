from fastapi import FastAPI

from routers.auth.auth import router as auth_login

def setup_routers(app: FastAPI):
    app.include_router(auth_login)
