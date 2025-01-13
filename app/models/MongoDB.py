import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db():
    """
    This function returns the MongoDatabase instance.
    """
    return MongoDatabase()


class MongoDatabase:
    def __init__(self):
        # Establish the connection on class instantiation
        self.client = self.check_mongo_connection()
        self.db = self.client[os.getenv("MONGO_DATABASE")]
        self.teachers_collection = self.db["Teachers"]
        self.lessons_collection = self.db["Lessons"]
        self.CalendarEvents=self.db["CalendarEvents"]
        self.suggestions_collection=self.db["suggestions_collection"]
        self.support_collection=self.db["support_collection"]

    def check_mongo_connection(self):
        """
        This function checks the MongoDB connection using a single URI from environment variables.
        """
        # Get the MongoDB URI directly from environment variables
        mongo_uri = os.getenv("MONGO_CLUSTER_URL")

        # Validate that the URI is set
        if not mongo_uri:
            raise KeyError("MongoDB URI is not set/loaded correctly.")

        # Attempt to establish a connection
        try:
            client = MongoClient(mongo_uri)
            # Send a ping to check if the connection is successful
            client.admin.command('ping')
            print("Connection to MongoDB successful!")
            return client
        except Exception as e:
            print(f"Error connecting to MongoDB: {str(e)}")
            raise Exception(f"MongoDB connection failed: {str(e)}")

# Example usage
mongo_db = get_db()
