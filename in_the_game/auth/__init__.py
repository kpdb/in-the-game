from fastapi import APIRouter, Body, HTTPException

from .models import UserLogin, TokenResponse
from . import service

router = APIRouter()


@router.post("/login", response_model=TokenResponse, status_code=201)
async def login_user(login_data: UserLogin = Body(...)):
    response = await service.login_user(login_data)
    if not response:
        raise HTTPException(status_code=403, detail="Incorrect user credentials")
    return response
