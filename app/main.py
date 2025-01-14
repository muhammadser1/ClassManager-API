from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, teacher, admin,event
# Initialize FastAPI app
app = FastAPI(
    title="Teacher Management System",
    description="An application to manage teacher and admin workflows for your institute.",
    version="1.0.0",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(teacher.router, prefix="/teacher", tags=["Teacher"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(event.router, prefix="/event", tags=["event"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Teacher Management System!"}
