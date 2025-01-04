from fastapi import APIRouter, HTTPException, status, Depends, Request
from pymongo import MongoClient
from app.models.MongoDB import mongo_db
from app.schemas.user import LoginRequest, SignupRequest, ResetPasswordRequest
from app.services.teacher_service import add_teacher_to_db
from app.utils.email_utils import generate_reset_token, send_reset_email
from app.utils.password import hash_password, verify_password
from app.models.teacher import Teacher
from datetime import datetime, timedelta
from typing import List

router = APIRouter()


@router.post("/login-teacher")
async def login_teacher(request: LoginRequest):
    teacher = mongo_db.teachers_collection.find_one({"name": request.name})
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(request.password, teacher['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"message": "Login successful"}


@router.post("/signup-teacher")
async def signup_teacher(request: SignupRequest):
    name = request.name
    email = request.email
    password = request.password

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


@router.post("/forgot-password")
async def forgot_password_teacher(request: Request):
    email = request.query_params.get("email")  # Get email from query string
    teacher = mongo_db.teachers_collection.find_one({"email": email})

    if not teacher:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate reset token and store it in the database
    reset_token = generate_reset_token()
    expiration_time = datetime.utcnow() + timedelta(hours=1)

    mongo_db.teachers_collection.update_one(
        {"email": email},
        {"$set": {"reset_token": reset_token, "reset_token_expiry": expiration_time}}
    )

    send_reset_email(email, reset_token, teacher['name'])  # Send reset email

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


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    token = request.token
    password = request.password

    # Retrieve the teacher by reset token from MongoDB
    teacher = mongo_db.teachers_collection.find_one({"reset_token": token})

    if not teacher:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Check if the token has expired
    if teacher["reset_token_expiry"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token has expired")

    # Hash the new password
    hashed_password = hash_password(password)

    # Update the password in the database (update the hashed_password field)
    result = mongo_db.teachers_collection.update_one(
        {"reset_token": token},
        {"$set": {
            "hashed_password": hashed_password,  # Store the hashed password
            "reset_token": None,  # Invalidate the token
            "reset_token_expiry": None  # Invalidate the expiry
        }}
    )

    # Check if the update was successful
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update password in the database")

    return {"message": "Password has been successfully reset"}
