# email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import random
import string
load_dotenv()


# Function to send reset email
def send_reset_email(to_email: str, token: str, name: str):
    # Configure SMTP server (e.g., using Gmail's SMTP)
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver_email = to_email
    # Create the email content
    subject = "Password Reset Request"
    body = f"""
    Dear {name},

    We received a request to reset your password. Click the link below to reset your password:

    http://your-frontend-url/reset-password?token={token}

    If you did not request a password reset, please ignore this email.

    Regards,
    Your Institute
    """
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


# Function to generate a random reset token
def generate_reset_token() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))