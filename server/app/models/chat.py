from bson import ObjectId
from app.extensions import mongo
from datetime import datetime
from datetime import datetime
from zoneinfo import ZoneInfo  # or use pytz for Python < 3.9


class Chat:
    @staticmethod
    def start_or_update_conversation(ownid, user_name, user_msg, bot_msg, conversation_id=None, business_id=None,
                                     resource_id=None, taxonomy_id=None, date = None):
        message_pair = [
            {"from": user_name, "text": user_msg},
            {"from": "bot", "text": bot_msg}
        ]

        if conversation_id:
            mongo.db.chats.update_one(
                {"_id": ObjectId(conversation_id)},
                {
                    "$push": {"messages": {"$each": message_pair}},
                    "$set": {
                        "business_id": business_id,
                        "resource_id": resource_id,
                        "taxonomy_id": taxonomy_id,
                        "date": date
                    }
                }
            )
            return conversation_id
        else:
            current_msg_time = datetime.now(ZoneInfo("Asia/Jerusalem"))  # 🕒 Israeli time
            chat_entry = {
                "ownid": ownid,
                "messages": message_pair,
                "created_at": current_msg_time.isoformat(),
                "business_id": business_id,
                "resource_id": resource_id,
                "taxonomy_id": taxonomy_id,
                "date": date

            }
            result = mongo.db.chats.insert_one(chat_entry)
            return str(result.inserted_id)

    @staticmethod
    def get_user_chats(ownid):
        chats = mongo.db.chats.find({"ownid": ownid}).sort("created_at", -1)
        chat_list = []
        for chat in chats:
            chat["_id"] = str(chat["_id"])  # Convert ObjectId to string
            chat_list.append(chat)
        return chat_list

    @staticmethod
    def get_patient_business_id(conversation_id):
        chat = mongo.db.chats.find_one({"_id": ObjectId(conversation_id)})
        if chat:
            return chat.get("business_id")
        return None

    @staticmethod
    def get_patient_resource_id(conversation_id):
        chat = mongo.db.chats.find_one({"_id": ObjectId(conversation_id)})
        if chat:
            return chat.get("resource_id")
        return None

    @staticmethod
    def get_patient_toxonomy_id(conversation_id):
        chat = mongo.db.chats.find_one({"_id": ObjectId(conversation_id)})
        if chat:
            return chat.get("taxonomy_id")
        return None
    
    @staticmethod
    def get_patient_date(conversation_id):
        chat = mongo.db.chats.find_one({"_id": ObjectId(conversation_id)})
        if chat:
            return chat.get("date")
        return None

    @staticmethod
    def get_business_name(conversation_id):
        chat = mongo.db.chats.find_one({"_id": ObjectId(conversation_id)})
        if chat:
            return chat.get("business_name")
        return None
    
    @staticmethod
    def get_resource_name(conversation_id):
        chat = mongo.db.chats.find_one({"_id": ObjectId(conversation_id)})
        if chat:
            return chat.get("resource_name")
        return None
    
    @staticmethod
    def get_taxonomy_name(conversation_id):
        chat = mongo.db.chats.find_one({"_id": ObjectId(conversation_id)})
        if chat:
            return chat.get("taxonomy_name")
        return None

    @staticmethod
    def set_patient_business_id(conversation_id, business_id):
        mongo.db.chats.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"business_id": business_id}}
        )

    @staticmethod
    def set_patient_resource_id(conversation_id, resource_id):
        mongo.db.chats.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"resource_id": resource_id}}
        )

    @staticmethod
    def set_patient_taxonomy_id(conversation_id, taxonomy_id):
        mongo.db.chats.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"taxonomy_id": taxonomy_id}}
        )

    @staticmethod
    def set_patient_date(conversation_id, date):
        mongo.db.chats.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"date": date}}
        )

    @staticmethod
    def set_patient_time(conversation_id, time):
        chat = mongo.db.chats.find_one({"_id": ObjectId(conversation_id)})
        if chat:
            date = chat.get("date")
        print("date ", date)
        date_and_time = date + "T" + str(time) + ":00"
        print("date_and_time ",date_and_time)
        mongo.db.chats.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"date": date_and_time}}
        )

        
    @staticmethod
    def set_business_name(conversation_id, business_name):
        mongo.db.chats.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"business_name": business_name}}
        )


    @staticmethod
    def set_resource_name(conversation_id, resource_name):
        mongo.db.chats.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"resource_name": resource_name}}
        )


    @staticmethod
    def set_taxonomy_name(conversation_id, taxonomy_name):
        mongo.db.chats.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"taxonomy_name": taxonomy_name}}
        )