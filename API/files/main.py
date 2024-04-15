from fastapi import FastAPI, Depends

from API.files.router import router

# from preprocessing.src.operations.router import router as router_operation

app = FastAPI(
    title="SAM",
    description="",
    summary="",
    version="1.0",
    root_path="/api"
)

app.include_router(router)
