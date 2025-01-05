from fastapi import APIRouter
from starlette.responses import HTMLResponse, JSONResponse
import arabic_reshaper
from bidi.algorithm import get_display
from app.schemas.lesson import Lesson

router = APIRouter()

@router.post("/submit-lesson")
async def submit_lesson(lesson: Lesson):
    # Print the received data to the console in Arabic
    teacher_name = arabic_reshaper.reshape(lesson.teacherName)
    student_name = arabic_reshaper.reshape(lesson.studentName)
    education_level = arabic_reshaper.reshape(lesson.educationLevel)
    subject = arabic_reshaper.reshape(lesson.subject)
    date = arabic_reshaper.reshape(lesson.date)

    print("Teacher Name:", get_display(teacher_name))
    print("Student Name:", get_display(student_name))
    print("Hours:", lesson.hours)
    print("Education Level:", get_display(education_level))
    print("Subject:", get_display(subject))
    print("Date:", get_display(date))

    # Return the data as a JSON response
    return JSONResponse(content={
        "message": "بيانات الدرس تم استقبالها وطبعها",
        "lesson_data": {
            "teacherName": lesson.teacherName,
            "studentName": lesson.studentName,
            "hours": lesson.hours,
            "educationLevel": lesson.educationLevel,
            "subject": lesson.subject,
            "date": lesson.date
        }
    })

@router.get("/dashboard")
async def dashboard():
    return {"message": "Teacher dashboard endpoint"}


@router.put("/edit-lesson/{lesson_id}")
async def edit_lesson(lesson_id: int):
    return {"message": f"Edit lesson endpoint for lesson_id {lesson_id}"}


@router.delete("/delete-lesson/{lesson_id}")
async def delete_lesson(lesson_id: int):
    return {"message": f"Delete lesson endpoint for lesson_id {lesson_id}"}
