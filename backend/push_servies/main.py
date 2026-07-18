import asyncio
from datetime import datetime, timezone
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from db import AsyncSessionLocal, get_db
from repository.chats import get_chat_id, get_receiver_id
from schemas.message import MessageCreate
from services.producer_message import producer_message
from services.consumer_message import consume_messages
from services.token import  verify_ws_token
from websocket.manager import manager

from fastapi import FastAPI
import uvicorn

from kafka_client import start_kafka, stop_kafka

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
print("MAIN.PY ЗАГРУЖЕН")
consumer_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):

    global consumer_task


    await start_kafka()


    consumer_task = asyncio.create_task(
        consume_messages()
    )


    logging.info(
        "Kafka consumer started"
    )


    yield


    if consumer_task:
        consumer_task.cancel()

        try:
            await consumer_task
        except asyncio.CancelledError:
            pass


    await stop_kafka()


app = FastAPI(
    lifespan=lifespan
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    try:
        data_token = verify_ws_token(token)
    except Exception as e:
        logging.error(f"Ошибка проверки токена: {e}")
        await websocket.close(code=1008)
        return

    user_id = data_token["user_id"]

    await manager.connect(user_id, websocket)

    async with AsyncSessionLocal() as db:
        try:
            while True:
                data = await websocket.receive_json()

                chat_id = await get_chat_id(
                    data["chat_id"],
                    db
                )

                receiver_id = await get_receiver_id(
                    chat_id,
                    user_id,
                    db
                )

                result = await producer_message(
                    chat_id,
                    data["text"],
                    user_id,
                    data_token["username"],
                    receiver_id
                )

                if "error" in result:
                    logging.error(f"Ошибка отправки сообщения: {result['error']}")
                    continue  # не отправляем сообщение дальше, если произошла ошибка

                outgoing = {
                    "chat_id": data["chat_id"],  # ← используем исходный public_id от клиента, а не внутренний int
                    "id": str(result["id"]),
                    "text": data["text"],
                    "sender_id": str(user_id),
                    "sender_name": data_token["username"],
                    "receiver_id": str(receiver_id),
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "client_id": data.get("client_id"),
                }
                logging.info(f"sender={user_id} ({type(user_id)}), receiver={receiver_id} ({type(receiver_id)})")
                logging.info(f"активные соединения: {list(manager.connections.keys())}")
                await manager.send(user_id, outgoing)
                await manager.send(receiver_id, outgoing)
        except WebSocketDisconnect:
            manager.disconnect(user_id)
        except Exception as e:
            logging.error(f"Ошибка обработки сообщения: {e}")
            manager.disconnect(user_id)
            await websocket.close(code=1011)


@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003, ws="websockets")