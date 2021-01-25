from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from in_the_game import auth, healthcheck, teams, users
from in_the_game.db import database

ORIGINS = [
    "http://localhost",
]

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(healthcheck.router, prefix="/health", tags=["health"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(users.router, prefix="/users", tags=["users"])

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
