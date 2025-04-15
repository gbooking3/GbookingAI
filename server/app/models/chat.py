from bson import ObjectId
from app.extensions import mongo
from datetime import datetime
from datetime import datetime
from zoneinfo import ZoneInfo  # or use pytz for Python < 3.9

class Chat:
    @staticmethod
    def start_or_update_conversation(ownid, user_name, user_msg, bot_msg, conversation_id=None):
        message_pair = [
            {"from": user_name, "text": user_msg},
            {"from": "bot", "text": bot_msg}
        ]

        if conversation_id:
            mongo.db.chats.update_one(
                {"_id": ObjectId(conversation_id)},
                {"$push": {"messages": {"$each": message_pair}}}
            )
            return conversation_id
        else:
            current_msg_time = datetime.now(ZoneInfo("Asia/Jerusalem"))  # 🕒 Israeli time
            chat_entry = {
                "ownid": ownid,
                "messages": message_pair,
                "created_at": current_msg_time.isoformat()
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
