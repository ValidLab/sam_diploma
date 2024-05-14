from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from API.files.router import router


app = FastAPI(
    title="SAM",
    description="",
    summary="",
    version="1.0",
    root_path="/api"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.56.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_credentials=True,
    expose_headers=['Content-Disposition'],
)

app.include_router(router)
