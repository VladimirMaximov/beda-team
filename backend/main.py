from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # todo: delete

from backend.routers import router
from backend.configurations.database import create_db_and_tables, global_init



@asynccontextmanager
async def lifespan(app: FastAPI):
    global_init()  # todo: add global_init func
    await create_db_and_tables()
    yield

app = FastAPI(
    title="Recipe Matcher API",
    description="API for getting recipes by ingredients list",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(  # todo: delete
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


