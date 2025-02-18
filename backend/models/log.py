from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client['parking']
log_collection = db['logs']

    
class Log:
    def __init__(self, action, description, plate=None, zone=None, date_in=None, date_out=None, timestamp=None):
        self.action = action
        self.description = description
        self.plate = plate
        self.zone = zone
        self.time_in = date_in
        self.time_out = date_out
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def save_log(cls, log):
        log_data = {
            "action": log.action,
            "description": log.description,
            "plate": log.plate,
            "zone": log.zone,
            "date_in": log.date_in,
            "date_out": log.date_out,
            "timestamp": log.timestamp
        }
        
        log_collection.insert_one(log_data)
        
        return log


    @classmethod
    def get_logs(cls, filter=None, limit=None):
        if filter is None:
            filter = {}
        cursor = log_collection.find(filter).sort("timestamp", -1)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)

    @classmethod
    def clear_logs(cls):
        log_collection.delete_many({})
