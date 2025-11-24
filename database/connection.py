from pymongo import MongoClient
import config

client = MongoClient(config.settings.MONGO_URI)
db = client[config.settings.DB_NAME]
