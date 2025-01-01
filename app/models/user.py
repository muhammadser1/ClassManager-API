from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    name = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    reset_token = Column(String, nullable=True)  # New field for the reset token
    reset_token_expiry = Column(DateTime, nullable=True)  # New field for expiration time
