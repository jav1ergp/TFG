from pymongo import MongoClient
from datetime import datetime
from config.back_config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
log_collection = db['logs']

    
class Log:
    def __init__(self, action, description, plate, zona, timestamp=None):
        self.action = action
        self.description = description
        self.plate = plate
        self.zona = zona
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def save_log(cls, log):
        log_data = {
            "action": log.action,
            "description": log.description,
            "plate": log.plate,
            "zona": log.zona,
            "timestamp": log.timestamp
        }
        
        log_collection.insert_one(log_data)
        
        return log
