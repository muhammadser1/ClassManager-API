# utils/password.py
import random
import string

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the plain password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# Function to generate a random reset token
def generate_reset_token() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))
