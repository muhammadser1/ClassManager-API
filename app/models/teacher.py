import datetime

from app.models.MongoDB import mongo_db


class Teacher:
    def __init__(self, name: str, email: str, hashed_password: str, birthday: datetime.date, is_admin: bool = False,
                 reset_token: str = None, reset_token_expiry: datetime = None, last_lesson_number: int = 0):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_admin = is_admin
        self.reset_token = reset_token
        self.reset_token_expiry = reset_token_expiry
        self.last_lesson_number = last_lesson_number  # Track the last lesson number for the teacher
        self.birthday=birthday
    def to_dict(self):
        """
        Convert the Teacher instance to a dictionary to be saved in MongoDB.
        """
        return {
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_admin": self.is_admin,
            "reset_token": self.reset_token,
            "reset_token_expiry": self.reset_token_expiry,
            "last_lesson_number": self.last_lesson_number,  # Save the last lesson number
        "birthday": self.birthday.isoformat() if self.birthday else None,  # Ensure birthday is saved as ISO string

        }

    def generate_lesson_id(self):
        """
        Generate a unique lesson ID for this teacher.
        """
        # Increment the lesson number
        self.last_lesson_number += 1

        # Update the teacher's last lesson number in the database
        mongo_db.teachers_collection.update_one(
            {"name": self.name},
            {"$set": {"last_lesson_number": self.last_lesson_number}},
            upsert=True
        )

        # Generate lesson ID based on teacher's name and the incremented lesson number
        lesson_id = f"{self.name}_{self.last_lesson_number}"
        return lesson_id