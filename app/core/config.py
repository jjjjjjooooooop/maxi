import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Support Chat Bot"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./support_chat.db")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-before-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60


settings = Settings()
