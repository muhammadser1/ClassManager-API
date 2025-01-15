
# ClassManager-API

## Overview

ClassManager-API is a lesson management system designed to function similarly to Moodle. This system facilitates efficient lesson tracking and management for teachers and administrators. Teachers and admins can easily submit their lessons, monitor progress, and calculate the total teaching hours per education level. The platform aims to streamline administrative tasks and enhance the organization of educational activities.

## Technologies

### Backend:

-   **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
    
-   **MongoDB**: A NoSQL database used for storing lesson and user data efficiently.
    

## Environment Variables

The following environment variables should be set in a `.env` file located in the root directory of your project:

-   `EMAIL_USER`: Your email address for sending system emails.
    
-   `EMAIL_PASSWORD`: The password or app-specific password for the email account.
    
-   `MONGO_DATABASE`: The name of your MongoDB database.
    
-   `MONGO_CLUSTER_URL`: The MongoDB connection URL.
    
-   `SECRET_KEY`: A secret key used for hashing.
    

## How to Run
1. Install the required dependencies:
```python
pip install -r requirements.txt
```
2. Start the development server:
```python
uvicorn app.main:app --reload
```
