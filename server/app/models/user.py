from app.extensions import mongo
from pymongo import MongoClient, ReturnDocument



class User:


    @staticmethod
    def find_by_ownid(ownid):
        return mongo.db.users.find_one({"ownid": ownid})
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_by_phone(phone):
        return mongo.db.users.find_one({"phone": phone})

    @staticmethod
    def find_by_email_or_phone(id_value):
        return mongo.db.users.find_one({
            "$or": [{"email": id_value}, {"phone": id_value}]
        })
    @staticmethod
    def reactivate_user(ownid):
        mongo.db.users.update_one(
            {"ownid": ownid},
            {"$set": {"is_active": True}}
        )


    @staticmethod
    def find_by_ownid_and_phone(ownid):
        return mongo.db.users.find_one({
            "$and": [{"ownid": ownid}]
        })

    @staticmethod
    def delete_by_ownid(ownid):
        result = mongo.db.users.update_one(
            {"ownid": ownid},
            {"$set": {"is_active": False}}
        )
        return result.modified_count > 0

    @staticmethod
    def create_user(data):
        counters = mongo.db.counters
        print(counters)
        # Increment the clientid atomically and get the updated counter
        counter = counters.find_one_and_update(
            {"_id": "userClientId"},
            {"$inc": {"seq": 1}},
            return_document=True)
        new_clientid = counter["seq"]
        user_data = {
            "name": data["name"],
            "email": data["email"],
            "phone": data["phone"],
            "ownid": data["ownid"],
            "clientid": new_clientid,
            "is_active": True
        }
        return mongo.db.users.insert_one(user_data)

    @staticmethod
    def update_user_name(data):
        result = mongo.db.users.update_one(
            {'ownid': data['ownid']},
            {'$set': {'name': data['name']}}
        )
        return result.modified_count > 0

    @staticmethod
    def to_json(user):
        return {
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "ownid": user["ownid"]
        }



