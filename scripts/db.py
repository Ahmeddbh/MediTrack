from pymongo import MongoClient

def get_collection():
    client = MongoClient("mongodb://localhost:27017/")
    return client["meditrack"]["pacientes"]