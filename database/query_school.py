from __future__ import print_function
from pymongo import MongoClient

client = MongoClient() #create connection to MongoDB

db = client['capstone'] #selects 
school_coll = db.school

school_info = {}

school_name = raw_input("What school do you want to look up? ")

school_info = school_coll.find({"INSTNM": school_name})

for parts in school_info:
	for part in parts:
		print(part, end=': ') # print column name
		print(parts[part]) #print value of column


