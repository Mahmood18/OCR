# Code to Setup Mongo Db and methods for operations on the MongoDB
import os
import datetime
from config import *
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from urllib.parse import urlparse, quote_plus


# Class for creating connection with MongoDB 
class MongoDBConnection:
    """Class Mongo DB is used to create Connection with the Mongo DB using the connection string in the 
    enviornment File"""
    def __init__(self):
        self.uri = MONGO_DB_URI
        self.client = None

    def __enter__(self):
        self.client = MongoClient(self.uri)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

class MongoDBOperations:
    """Class is used to perform operation ons a Given Mongo DB and collection on the connected 
    Mongo DB using the URI
    """
    def __init__(self, dbname, collname):
        self.dbname = dbname
        self.collname = collname

    def insert_document(self, document)->bool:
        document['created_at'] = str(datetime.datetime.utcnow())
        try:
            with MongoDBConnection() as connection:
                db = connection[self.dbname]
                collection = db[self.collname]
                collection.insert_one(document)
                print("Document inserted")
            return True
        except PyMongoError as e:
            print(f'An error occurred while inserting a document: {e}')
            return False
    
    def insert_documents(self, documents)->bool:
        for document in documents:
            document['created_at'] = str(datetime.datetime.utcnow())  # Add 'created_at' timestamp to each document
        try:
            with MongoDBConnection() as connection:
                db = connection[self.dbname]
                collection = db[self.collname]
                result = collection.insert_many(documents)
                return True
        except PyMongoError as e:
            print(f'An error occurred while inserting documents: {e}')
            return False


    def find_document(self, query)->dict:
        try:
            with MongoDBConnection() as connection:
                db = connection[self.dbname]
                collection = db[self.collname]
                return collection.find_one(query)
        except PyMongoError as e:
            print(f'An error occurred while finding a document: {e}')
            return None
        
    def find_documents(self, query)->list:
        try:
            with MongoDBConnection() as connection:
                db = connection[self.dbname]
                collection = db[self.collname]
                # Use list() to fetch all documents into memory while the connection is open
                return list(collection.find(query))
        except PyMongoError as e:
            print(f'An error occurred while finding the documents: {e}')
            return None
    
    def update_document(self, query, update_fields)->bool:
        try:
            with MongoDBConnection() as connection:
                db = connection[self.dbname]
                collection = db[self.collname]

                # Use list() to fetch all documents into memory while the connection is open
                collection.update_one(query,{'$set': update_fields}, upsert=False)
                return True
        except PyMongoError as e:
            print(f'An error occurred while updating the documents: {e}')
            return False
        
    def delete_document(self, query)->bool:
        try:
            with MongoDBConnection() as connection:
                db = connection[self.dbname]
                collection = db[self.collname]
                result = collection.delete_one(query)
                return True
        except PyMongoError as e:
            print(f'An error occurred while deleting a document: {e}')
            return False
    
    def delete_documents(self, query)->bool:
        try:
            with MongoDBConnection() as connection:
                db = connection[self.dbname]
                collection = db[self.collname]
                result = collection.delete_many(query)
                return True
        except PyMongoError as e:
            print(f'An error occurred while deleting documents: {e}')
            return False
        

        

