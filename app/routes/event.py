from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Query

from app.models.MongoDB import mongo_db
from app.schemas.event import Event

router = APIRouter()


@router.get("/events")
async def get_events():
    """
    Fetch all events from the database for the calendar.
    """
    try:
        # Query all events from the CalendarEvents collection
        events_cursor = mongo_db.db["CalendarEvents"].find()
        events = [
            {
                "id": str(event["_id"]),
                "title": event["title"],
                "teacher": event["teacher"],
                "date": event["date"].isoformat() if isinstance(event["date"], datetime) else str(event["date"]),
                "hours": event["hours"]
            }
            for event in events_cursor
        ]

        return events  # FastAPI will handle the JSON serialization

    except Exception as e:
        print("Error fetching events:", e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching events.")