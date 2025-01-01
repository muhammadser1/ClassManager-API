from fastapi import APIRouter

router = APIRouter()


@router.get("/approve-lessons")
async def approve_lessons():
    return {"message": "Approve lessons endpoint"}


@router.get("/analytics")
async def analytics():
    return {"message": "Admin analytics endpoint"}


@router.post("/send-email")
async def send_email():
    return {"message": "Send email endpoint"}
