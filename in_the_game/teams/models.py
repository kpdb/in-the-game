from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class NewTeam(BaseModel):
    name: str
    description: str
    country_code: str
    group: Optional[str]
    organization: Optional[str]


class Team(NewTeam):
    id: int


class MeetingBase(BaseModel):
    description: str
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: datetime = Field(default=None)


class NewMeeting(MeetingBase):
    team_ids: List[int]


class Meeting(MeetingBase):
    id: int
    teams: List[Team]
