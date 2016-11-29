#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

# CRUD
# create
# 1. create a connection
client = MongoClient("mongodb://localhost:27017")
#default connect to mongodb://localhost:27017
#client = MongoClient()

# 2. access database objects, remote database object assign to local db
db = client.test
#db = client['test'] dictionary-style

# 3. access collection objects
coll = db.restaurants
#coll = db['restaurants']



# update
from datetime import datetime
'''
The operation returns an InsertOneResult object, 
which includes an attribute inserted_id that contains the _id of the inserted document. 
Access the inserted_id attribute:

result = coll.insert_one(
	{
		"address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"

	}
)
print(result.inserted_id)
'''

# read
# query by a top level field
cursor = db.restaurants.find({"borough": "Manhattan"})
for document in cursor:
	print(document)

# query by a field in an embedded document,use dot notation
cursor = db.restaurants.find({"address.zipcode": "10075"})
for document in cursor:
	print(document)
