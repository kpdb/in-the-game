from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from in_the_game import healthcheck, teams
from in_the_game.db import database

ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8002",
    "http://localhost:5000",
]

app = FastAPI()
app.include_router(healthcheck.router, prefix="/health", tags=["health"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
