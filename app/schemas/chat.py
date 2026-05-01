from datetime import datetime

from pydantic import BaseModel, Field


class SessionRead(BaseModel):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    session_id: int = Field(gt=0)
    text: str = Field(min_length=1, max_length=1000)


class MessageRead(BaseModel):
    id: int
    sender: str
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}


class BotResponse(BaseModel):
    session_id: int
    user_message: MessageRead
    bot_message: MessageRead


class HistoryResponse(BaseModel):
    session_id: int
    messages: list[MessageRead]
