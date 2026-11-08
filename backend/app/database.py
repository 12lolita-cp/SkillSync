import os
from pymongo import MongoClient

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "skillsync_db"
)

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

users_collection = db["users"]
skills_collection = db["skills"]
certifications_collection = db["certifications"]