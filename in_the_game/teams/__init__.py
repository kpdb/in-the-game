from typing import List

from fastapi import APIRouter

from .models import NewTeam, Team, NewMeeting, Meeting
from . import service

router = APIRouter()


@router.get("/", response_model=List[Team])
async def get_all_teams():
    return await service.get_all_teams()

