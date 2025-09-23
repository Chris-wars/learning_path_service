import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27077")
MONGO_DB = os.getenv("MONGO_DB", "learning_paths")

mongo = MongoClient(MONGO_URI)
db = mongo[MONGO_DB]
paths = db["learning_paths"]

def ping() -> bool:
    # Der ping-Befehl ist eine einfache Möglichkeit, die Verbindung zu testen
    mongo.admin.command('ping')
    return True
