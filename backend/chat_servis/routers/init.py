from fastapi import FastAPI

from routers.messages import router as messages
from routers.chats import router as chats

def setup_routers(app: FastAPI):
    app.include_router(messages)
    app.include_router(chats)
