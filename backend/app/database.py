import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "skillsync_db")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

database = client[DATABASE_NAME]

users_collection = database["users"]
skills_collection = database["skills"]
certifications_collection = database["certifications"]


def test_connection():
    client.admin.command("ping")
    return True