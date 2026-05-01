from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.message import Message
from app.models.session import ChatSession
from app.models.user import User
from app.schemas.chat import BotResponse, HistoryResponse, MessageCreate, SessionRead
from app.services.bot import build_bot_reply

router = APIRouter(prefix="/chat", tags=["chat"])


def get_owned_session(session_id: int, user: User, db: Session) -> ChatSession:
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.user_id == user.id)
        .first()
    )
    if session is None:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session


@router.post("/session", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
async def create_session(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> ChatSession:
    session = ChatSession(user_id=current_user.id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.post("/message", response_model=BotResponse)
async def send_message(
    payload: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BotResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Message text cannot be empty")
    session = get_owned_session(payload.session_id, current_user, db)
    user_message = Message(session_id=session.id, sender="user", text=text)
    bot_message = Message(
        session_id=session.id, sender="bot", text=build_bot_reply(text)
    )
    db.add_all([user_message, bot_message])
    db.commit()
    db.refresh(user_message)
    db.refresh(bot_message)
    return BotResponse(
        session_id=session.id,
        user_message=user_message,
        bot_message=bot_message,
    )


@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HistoryResponse:
    session = get_owned_session(session_id, current_user, db)
    return HistoryResponse(session_id=session.id, messages=session.messages)
