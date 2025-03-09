import os
from pymongo import MongoClient
import urllib.parse

"""
class ProspectData(object):
     CRUD operations for College Prospects collection in MongoDB

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        if username and password:
            user = urllib.parse.quote_plus(username)
            passwd = urllib.parse.quote_plus(password)
            self.client = MongoClient(
                'mongodb://%s:%s@localhost:27017/DodgersDB?authSource=admin' % (user, passwd))
            #self.client = MongoClient('mongodb://localhost:27017')
            databaseName = 'DodgersDB'
            self.database = self.client[databaseName]
            print("Authentication Successful\nConnected to " + databaseName)
        else:
            print("Authentication Failed!")
            # Connect without authentication
            # self.client = MongoClient('mongodb://localhost:55711/AAC')
            # Connect with authentication, where xxxx is your unique port number
            #self.client = MongoClient('mongodb://%s:%s@localhost:xxxxx' % (username, password))
            #self.database = self.client['project']
            #print("Connection Successful")

"""
class ProspectData(object):
     """CRUD operations for College Prospects collection in MongoDB"""
     def __init__(self, mongo_uri):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        if mongo_uri:
            self.client = MongoClient(mongo_uri)
            databaseName = 'prospectDB'                       
            self.database = self.client[databaseName]
            print("Authentication Successful\nConnected to " + databaseName)
        else:
            print("Authentication Failed!")

# Complete this create method to implement the C in CRUD.
     def create(self, data):
        if data is not None:
            self.database.prospects.insert_one(data)  # data should be dictionary     
            return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            return False

# Create method to implement the R in CRUD. 
     def read(self, data):
        if data is not None:
            cursor = self.database.prospects.find(data)
            return cursor # returns one document as a python dictionary
        else:
            raise Exception("Nothing to read, because data parameter is empty.")
    
     def read_all(self, data):
        if data is not None:
            cursor = self.database.prospects.find(data, {'_id':False}) ## returns pointer to a results list
            #for item in cursor:
            #   print(item)
            return cursor
        else:
            raise Exception("Noting to read, because data parameter is empty")

# Update method to implement the U in CRUD.
     def update(self, data, updateData):
        if data is not None:
            result = self.database.prospects.update_many(data, {"$set" : updateData})            
            return result.raw_result
        else:
            raise Exception("Nothing to update, because data parameter is empty")
    
# Delete method to implement the D in CRUD.
     def delete(self, data):
        if data is not None:
            result = self.database.prospects.delete_many(data)
            return result.raw_result
        else:
            raise Exception("Nothing to delete, because data parameter is empty")