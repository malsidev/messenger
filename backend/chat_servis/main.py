from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from routers.init import setup_routers
from contextlib import asynccontextmanager


from kafka_client import start_kafka, stop_kafka
from cassandra_client import cassandra


@asynccontextmanager
async def lifespan(app: FastAPI):
    await cassandra.connect()
    await start_kafka()

    yield

    await stop_kafka()
    await cassandra.close()



app = FastAPI(
    lifespan=lifespan
)



setup_routers(app) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://localhost:19006",
        "http://192.168.1.11:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return 'hello '

setup_routers(app)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True) 