from app import mongo
from datetime import datetime

class ContactMessage:
    @staticmethod
    def create(name, email, message):
        mongo.db.contact_messages.insert_one({
            "name": name,
            "email": email,
            "message": message,
            "timestamp": datetime.utcnow()
        })
