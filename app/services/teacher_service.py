from app.models.teacher import Teacher
from app.models.MongoDB import mongo_db

def add_teacher_to_db(teacher: Teacher):
    """
    Function to add a teacher to the MongoDB database.
    """
    teacher_data = teacher.to_dict()
    mongo_db.teachers_collection.insert_one(teacher_data)
