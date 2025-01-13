import jwt
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # This loads variables from the .env file

SECRET_KEY = os.getenv("SECRET_KEY")


# Function to create a JWT token
def create_access_token(data: dict):
    # Add the expiration time for the token (e.g., 1 hour)
    expiration = datetime.utcnow() + timedelta(hours=1)
    encoded_jwt = jwt.encode({"exp": expiration, **data}, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


