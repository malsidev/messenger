import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from kafka_client import consume

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

consumer_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global consumer_task
    consumer_task = asyncio.create_task(consume())
    logging.info("Kafka consumer started")
    yield
    # Shutdown
    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
    logging.info("Kafka consumer stopped")

app = FastAPI(title="Storage Service", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, ws="websockets")