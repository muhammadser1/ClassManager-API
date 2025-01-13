from pydantic import BaseModel, validator
from datetime import datetime


class Event(BaseModel):
    title: str
    teacher: str
    date: str
    hours: int

    @validator("date")
    def validate_and_convert_date(cls, value):
        """
        Validate and convert the input date from 'YYYY-MM-DDTHH:MM' to a datetime object.
        """
        try:
            # Parse the provided date string into a datetime object
            parsed_date = datetime.strptime(value, "%Y-%m-%dT%H:%M")
            return parsed_date
        except ValueError:
            raise ValueError("Date must be in the format 'YYYY-MM-DDTHH:MM'")

    @validator("hours")
    def validate_hours(cls, value):
        if value <= 0:
            raise ValueError("Hours must be a positive number.")
        return value
