from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime
from typing import Optional


class URLCreate(BaseModel):
    original_url: AnyHttpUrl


class URLResponse(BaseModel):
    original_url: AnyHttpUrl
    short_code: Optional[str] = None
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    status: str
    data: Optional[dict | list] = " "
    message: Optional[str] = "deleted URL successfully"