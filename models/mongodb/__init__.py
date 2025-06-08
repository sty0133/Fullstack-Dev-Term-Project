from pymongo import MongoClient
import os

MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)

# MongoDB 클라이언트 생성
DATABASE_NAME = os.getenv('DATABASE_NAME')
db = client[DATABASE_NAME]

DOCUMENT_COLLECTION = os.getenv('DOCUMENT_COLLECTION')
DOCUMENT_COLLECTION = db[DOCUMENT_COLLECTION]