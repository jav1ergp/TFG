from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client['parking']
log_collection = db['logs']

    
class Log:
    def __init__(self, action, description, plate, zone, date_in, date_out=None, timestamp=None):
        self.action = action
        self.description = description
        self.plate = plate
        self.zone = zone
        self.date_in = date_in
        self.date_out = date_out
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
    def clear_logs(cls):
        log_collection.delete_many({})
