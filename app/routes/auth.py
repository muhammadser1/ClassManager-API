from fastapi import APIRouter, HTTPException, status, Depends
from pymongo import MongoClient
from app.models.MongoDB import mongo_db
from app.services.teacher_service import add_teacher_to_db
from app.utils.email_utils import generate_reset_token, send_reset_email
from app.utils.password import hash_password, verify_password
from app.models.teacher import Teacher
from datetime import datetime, timedelta
from typing import List

router = APIRouter()


@router.post("/login-teacher")
async def login_teacher(name: str, password: str):
    teacher = mongo_db.teachers_collection.find_one({"name": name})

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(password, teacher['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"message": "Login successful"}


@router.post("/signup-teacher")
async def signup_teacher(name: str, email: str, password: str):
    # Check if the teacher already exists by email
    existing_teacher = mongo_db.teachers_collection.find_one({"email": email})
    if existing_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if the teacher already exists by username (name)
    existing_teacher_by_name = mongo_db.teachers_collection.find_one({"name": name})
    if existing_teacher_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Hash the password before storing
    hashed_password = hash_password(password)

    # Create a new Teacher object
    new_teacher = Teacher(name=name, email=email, hashed_password=hashed_password)

    # Add teacher to MongoDB
    add_teacher_to_db(new_teacher)

    return {"message": f"Teacher {new_teacher.name} created successfully"}


@router.post("/forgot-password-teacher")
async def forgot_password_teacher(email: str):
    # Check if the teacher exists
    teacher = mongo_db.teachers_collection.find_one({"email": email})

    if not teacher:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate reset token and store it in the database
    reset_token = generate_reset_token()
    expiration_time = datetime.utcnow() + timedelta(hours=1)

    # Store the reset token and expiration in the teacher record
    mongo_db.teachers_collection.update_one(
        {"email": email},
        {"$set": {"reset_token": reset_token, "reset_token_expiry": expiration_time}}
    )

    send_reset_email(email, reset_token, teacher['name'])

    return {"message": "Password reset email sent!"}


@router.get("/teachers", response_model=List[dict])
async def get_all_teachers():
    teachers_data = list(mongo_db.teachers_collection.find({}))
    if not teachers_data:
        raise HTTPException(status_code=404, detail="No teachers found in the database.")

    # Clean up the returned data (remove '_id' field which is added by MongoDB)
    for teacher in teachers_data:
        teacher.pop('_id', None)

    return teachers_data
