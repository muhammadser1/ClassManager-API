from pydantic import BaseModel


class Lesson(BaseModel):
    teacherName: str
    studentName: str
    hours: int
    educationLevel: str
    subject: str
    date: str