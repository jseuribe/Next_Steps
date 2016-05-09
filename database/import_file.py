from pymongo import MongoClient
from file_functions import parse_file

client = MongoClient() #create connection to MongoDB

db = client['capstone'] #selects 
user_coll = db.user
user_coll.remove()
user_file = open("sample_user.csv", "r")
user_list = list()
user_list = parse_file(user_file)
user_coll.insert(user_list)
user_file.close()


school_coll = db.school
school_coll.remove()
school_file = open("ny_schools_v2.csv", "r")
school_list = list()
school_list = parse_file(school_file)
school_coll.insert(school_list)
school_file.close()


major_coll = db.major
major_coll.remove()
major_file = open("major_mapping.csv", "r")
major_list = list()
major_list = parse_file(major_file)
major_coll.insert(major_list)
major_file.close()


degrees_coll = db.degrees
degrees_coll.remove()
degrees_file = open("degrees_mapping.csv", "r")
degrees_list = list()
degrees_list = parse_file(degrees_file)
degrees_coll.insert(degrees_list)
degrees_file.close()


region_coll = db.region
region_coll.remove()
region_file = open("region_mapping.csv", "r")
region_list = list()
region_list = parse_file(region_file)
region_coll.insert(region_list)
region_file.close()


state_coll = db.state
state_coll.remove()
state_file = open("state_mapping.csv", "r")
state_list = list()
state_list = parse_file(state_file)
state_coll.insert(state_list)
state_file.close()