import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.admin.router import router as admin_router 
from src.rabbit.rabbit import consume

app = FastAPI(
    root_path="/admin" if os.getenv("DEV_SERV") == 'true' else None,
    docs_url="/docs" if os.getenv("ENV") == "dev" else None,
    redoc_url="/redoc" if os.getenv("ENV") == "dev" else None,
    openapi_url="/openapi.json" if os.getenv("ENV") == "dev" else None,
)
# CORS 미들웨어
origins = [
    "*",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    # use the same loop to consume
    asyncio.ensure_future(consume(loop))

# router
app.include_router(admin_router)


