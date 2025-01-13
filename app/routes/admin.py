from fastapi import APIRouter, HTTPException, Query

from app.models.MongoDB import mongo_db
from app.schemas.event import Event

router = APIRouter()


@router.put("/update-lesson-status/{lesson_id}")
async def update_lesson_status(
        lesson_id: str,
        status: str = Query(..., description="New status for the lesson ('approved' or 'rejected')")
):
    """
    Admin updates the status of a lesson. If rejected, delete the lesson.
    """
    try:
        # Validate the status
        if status not in ["approved", "rejected"]:
            raise HTTPException(status_code=400, detail="Invalid status. Use 'approved' or 'rejected'.")

        if status == "approved":
            # Update the status to 'approved'
            update_result = mongo_db.lessons_collection.update_one(
                {"lesson_id": lesson_id},
                {"$set": {"status": "approved"}}
            )

            if update_result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Lesson not found.")

            return {"message": f"Lesson {lesson_id} approved successfully."}

        elif status == "rejected":
            # Delete the lesson if rejected
            delete_result = mongo_db.lessons_collection.delete_one({"lesson_id": lesson_id})

            if delete_result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Lesson not found.")

            return {"message": f"Lesson {lesson_id} rejected and deleted successfully."}

    except Exception as e:
        print("Error updating lesson status:", e)
        raise HTTPException(status_code=500, detail="An error occurred while updating the lesson status.")


@router.get("/analytics")
async def analytics():
    return {"message": "Admin analytics endpoint"}


@router.post("/send-email")
async def send_email():
    return {"message": "Send email endpoint"}



@router.post("/add-event")
async def add_event(event: Event):
    """
    Add a new event to the database for the calendar.
    """
    try:
        # Convert Event object to a dictionary for MongoDB insertion
        event_data = {
            "title": event.title,
            "teacher": event.teacher,
            "date": event.date,  # Already converted to a datetime object by the validator
            "hours": event.hours
        }

        # Insert the event into the CalendarEvents collection
        result = mongo_db.db["CalendarEvents"].insert_one(event_data)

        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to add the event.")

        return {"message": "Event added successfully", "event_id": str(result.inserted_id)}

    except Exception as e:
        print("Error adding event:", e)
        raise HTTPException(status_code=500, detail="An error occurred while adding the event.")