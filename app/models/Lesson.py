from typing import Optional


class Lesson:
    def __init__(self, teacher_name: str, student_name: str, hours: int, education_level: str,
                 subject: str, date: str, lesson_id: Optional[int] = None, status: str = "pending"):
        self.lesson_id = lesson_id
        self.teacher_name = teacher_name
        self.student_name = student_name
        self.hours = hours
        self.education_level = education_level
        self.subject = subject
        self.date = date
        self.status = status  # 'pending' or 'approved'

    def to_dict(self):
        """
        Convert the Lesson instance to a dictionary to be saved in MongoDB.
        """
        return {
            "lesson_id": self.lesson_id,
            "teacher_name": self.teacher_name,
            "student_name": self.student_name,
            "hours": self.hours,
            "education_level": self.education_level,
            "subject": self.subject,
            "date": self.date,
            "status": self.status,
        }
