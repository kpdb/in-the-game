from typing import Optional, List

from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    firstname: str
    lastname: str
    country_code: str
    has_weekly_notifications: bool
    has_daily_notifications: bool
    has_live_notifications: bool
    notification_email: Optional[EmailStr]
    notification_url: Optional[str]
    team_ids: List[int]
