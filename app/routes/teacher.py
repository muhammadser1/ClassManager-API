from datetime import datetime  # Correctly import datetime
from typing import Optional

import bson
from fastapi import APIRouter, HTTPException, Request, Query
from starlette.responses import JSONResponse
import arabic_reshaper
from bidi.algorithm import get_display

from app.models.teacher import Teacher
from app.schemas.lesson import Lesson
from app.models.MongoDB import mongo_db
from datetime import datetime

from app.schemas.user import SuggestionRequest, SupportRequest
from app.utils.email_utils import send_suggest_email

router = APIRouter()


@router.post("/submit-lesson")
async def submit_lesson(request: Request):
    try:
        # Parse the JSON body
        data = await request.json()
        print("Received payload:", data)

        # Validate required field
        teacher_name = data.get("teacher_name")
        if not teacher_name:
            raise HTTPException(status_code=400, detail="Field 'teacher_name' is required.")

        # Fetch teacher from the database
        teacher_data = mongo_db.teachers_collection.find_one({"name": teacher_name})
        if not teacher_data:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Increment the last_lesson_number
        last_lesson_number = teacher_data.get("last_lesson_number", 0)  # Default to 0 if not set
        new_lesson_number = last_lesson_number + 1

        # Update the teacher's last_lesson_number in the database
        mongo_db.teachers_collection.update_one(
            {"name": teacher_name},
            {"$set": {"last_lesson_number": new_lesson_number}}
        )

        # Generate lesson_id
        lesson_id = f"{teacher_name}_{new_lesson_number}"
        print(f"Generated lesson_id: {lesson_id}")

        # Save the lesson to the database
        lesson_data = {
            "lesson_id": lesson_id,
            "teacher_name": teacher_name,
            "student_name": data["student_name"],
            "hours": data["hours"],
            "education_level": data["education_level"],
            "subject": data["subject"],
            "date": data["date"],
            "created_at": datetime.now(),
            "status": "pending",
        }
        inserted_result = mongo_db.lessons_collection.insert_one(lesson_data)

        # Add the _id as a string in the response if required
        lesson_data["_id"] = str(inserted_result.inserted_id)

        return {"message": "Lesson submitted successfully", "lesson_data": lesson_data}

    except Exception as e:
        print("Error processing request:", e)
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")


@router.get("/pending-lessons")
async def get_pending_lessons(teacher_name: Optional[str] = Query(None, description="Name of the teacher")):
    """
    Fetch pending lessons for a specific teacher if `teacher_name` is provided.
    If `teacher_name` is not provided, return all pending lessons.
    """
    try:
        # If `teacher_name` is provided, fetch lessons for the specific teacher
        query = {"status": "pending"}
        if teacher_name:
            query["teacher_name"] = teacher_name

        pending_lessons = list(mongo_db.lessons_collection.find(query, {"_id": 0}))  # Exclude `_id`

        if not pending_lessons:
            return {"message": "No pending lessons found.", "pending_lessons": []}

        return {"message": "Pending lessons retrieved successfully.", "pending_lessons": pending_lessons}

    except Exception as e:
        print("Error fetching pending lessons:", e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching pending lessons.")


@router.get("/approved-lessons")
async def get_approved_lessons(teacher_name: Optional[str] = Query(None, description="Name of the teacher")):
    """
    Fetch approved lessons for a specific teacher if `teacher_name` is provided.
    If `teacher_name` is not provided, return all approved lessons.
    """
    print(teacher_name,"  f")
    try:
        query = {"status": "approved"}
        if teacher_name:
            query["teacher_name"] = teacher_name

        approved_lessons = list(mongo_db.lessons_collection.find(query, {"_id": 0}))  # Exclude `_id`

        if not approved_lessons:
            return {"message": "No approved lessons found.", "approved_lessons": []}

        return {"message": "Approved lessons retrieved successfully.", "approved_lessons": approved_lessons}

    except Exception as e:
        print("Error fetching approved lessons:", e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching approved lessons.")


@router.put("/edit-lesson/{lesson_id}")
async def edit_lesson(
        lesson_id: str,
        request: Request,
        teacher_name: str = Query(..., description="Name of the teacher")
):
    """
    Edit a lesson's details based on lesson_id and teacher_name.
    """
    try:
        # Parse the JSON body for updates
        updated_data = await request.json()
        print("Received update data:", updated_data)

        # Validate that at least one field is being updated
        allowed_fields = {"student_name", "hours", "education_level", "subject", "date"}
        if not any(field in updated_data for field in allowed_fields):
            raise HTTPException(status_code=400, detail="No valid fields provided for update.")

        # Prepare the update query
        update_query = {"$set": {key: updated_data[key] for key in updated_data if key in allowed_fields}}

        # Find and update the lesson in the database
        update_result = mongo_db.lessons_collection.update_one(
            {"lesson_id": lesson_id, "teacher_name": teacher_name}, update_query
        )

        # Check if the lesson was found and updated
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Lesson not found or unauthorized to edit.")

        # Fetch the updated lesson
        updated_lesson = mongo_db.lessons_collection.find_one(
            {"lesson_id": lesson_id, "teacher_name": teacher_name},
            {"_id": 0}  # Exclude MongoDB's internal _id field from the response
        )

        return {"message": "Lesson updated successfully", "updated_lesson": updated_lesson}

    except Exception as e:
        print("Error editing lesson:", e)
        raise HTTPException(status_code=500, detail="An error occurred while editing the lesson.")


@router.delete("/delete-lesson/{lesson_id}")
async def delete_lesson(lesson_id: str, teacher_name: str = Query(..., description="Name of the teacher")):
    """
    Delete a lesson based on lesson_id and teacher_name.
    """
    try:
        # Find and delete the lesson
        delete_result = mongo_db.lessons_collection.delete_one(
            {"lesson_id": lesson_id, "teacher_name": teacher_name}
        )

        # Check if the lesson was found and deleted
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Lesson not found or unauthorized to delete.")

        return {"message": f"Lesson with ID {lesson_id} successfully deleted."}

    except Exception as e:
        print("Error deleting lesson:", e)
        raise HTTPException(status_code=500, detail="An error occurred while deleting the lesson.")


@router.post("/add-fake-lessons")
async def add_fake_lessons():
    try:
        teacher_name = "a"  # Replace with an existing teacher name in your database
        fake_lessons = [
            {
                "lesson_id": f"{teacher_name}_{i}",
                "teacher_name": teacher_name,
                "student_name": f"student_{i}",
                "hours": i + 1,
                "education_level": "High School",
                "subject": f"Subject {i}",
                "date": "2025-01-15",
                "created_at": datetime.now(),
                "status": "pending",
            }
            for i in range(1, 6)
        ]

        result = mongo_db.lessons_collection.insert_many(fake_lessons)
        return {"message": "Fake lessons added successfully.", "lesson_ids": [str(id) for id in result.inserted_ids]}
    except Exception as e:
        return {"error": str(e)}


@router.get("/teachers-birthdays")
async def get_teachers_with_birthday_today():
    today = datetime.today().strftime("%m-%d")  # Format to match MM-DD
    teachers = mongo_db.teachers_collection.find({})
    birthday_teachers = []

    for teacher in teachers:
        if "birthday" in teacher:
            teacher_birthday = datetime.fromisoformat(teacher["birthday"]).strftime("%m-%d")
            print(teacher_birthday,"    ",today)
            if teacher_birthday == today:
                birthday_teachers.append({"name": teacher["name"], "birthday": teacher["birthday"]})

    if not birthday_teachers:
        return {"message": "No birthdays today."}

    return {"birthday_teachers": birthday_teachers}

@router.post("/submit-suggestion")
async def submit_suggestion(msg: str):
    """
    Endpoint to submit a suggestion and send it via email.
    """
    try:
        print(msg)
        # Call the function to send the suggestion via email
        send_suggest_email(msg=msg)

        return {"message": "Suggestion submitted and sent via email successfully."}

    except Exception as e:
        print("Error submitting suggestion:", e)
        raise HTTPException(status_code=500, detail="An error occurred while submitting the suggestion.")


# @router.post("/submit-support-request")
# async def submit_support_request(support: SupportRequest):
#     """
#     Endpoint to submit a technical support request.
#     """
#     try:
#         # Prepare the support request data
#         support_data = {
#             "username": support.username,
#             "email": support.email,
#             "msg": support.msg,
#             "created_at": datetime.now(),
#         }
#
#         # Insert into the support collection
#         inserted_result = mongo_db.support_collection.insert_one(support_data)
#
#         return {"message": "Support request submitted successfully.", "support_request_id": str(inserted_result.inserted_id)}
#
#     except Exception as e:
#         print("Error submitting support request:", e)
#         raise HTTPException(status_code=500, detail="An error occurred while submitting the support request.")
