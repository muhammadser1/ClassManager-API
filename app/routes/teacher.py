from fastapi import APIRouter

router = APIRouter()


@router.post("/submit-lesson")
async def submit_lesson():
    return {"message": "Submit lesson endpoint"}


@router.get("/dashboard")
async def dashboard():
    return {"message": "Teacher dashboard endpoint"}


@router.put("/edit-lesson/{lesson_id}")
async def edit_lesson(lesson_id: int):
    return {"message": f"Edit lesson endpoint for lesson_id {lesson_id}"}


@router.delete("/delete-lesson/{lesson_id}")
async def delete_lesson(lesson_id: int):
    return {"message": f"Delete lesson endpoint for lesson_id {lesson_id}"}
