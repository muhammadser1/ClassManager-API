from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.user import User
from app.utils.email_utils import send_reset_email
from app.utils.password import hash_password, verify_password, generate_reset_token
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/login")
async def login(name: str, password: str, db: Session = Depends(get_db)):
    # Query the user by name (primary key)
    user = db.query(User).filter(User.name == name).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify if the provided password matches the stored hashed password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"message": "Login successful"}


@router.post("/signup")
async def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user_by_username = db.query(User).filter(User.name == username).first()
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Check if the email already exists
    existing_user_by_email = db.query(User).filter(User.email == email).first()
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # hashed password
    hashed_password = hash_password(password)

    # Create new user with username and email
    new_user = User(name=username, email=email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"User {new_user.name} created successfully"}


@router.post("/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    # Check if the user exists
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    # Generate reset token and store it in the database
    reset_token = generate_reset_token()
    expiration_time = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour

    # Store the reset token and expiration in the database (modify the User model if needed)
    user.reset_token = reset_token
    user.reset_token_expiry = expiration_time
    db.commit()

    # Send the reset email
    send_reset_email(user.email, reset_token, user.name)

    return {"message": "Password reset email sent!"}