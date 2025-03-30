from app.extensions import mongo

class User:
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
    def create_user(data):
        user_data = {
            "name": data["name"],
            "email": data["email"],
            "phone": data["phone"],
            "ownid": data["ownid"]
        }
        return mongo.db.users.insert_one(user_data)

   

    @staticmethod
    def to_json(user):
        return {
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "ownid": user["ownid"]
        }
