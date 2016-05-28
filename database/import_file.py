from pymongo import MongoClient
from file_functions import parse_file
import random
from datetime import datetime

client = MongoClient() #create connection to MongoDB

#Due to a lack of time, we currently randomly generate a list of majors
#That a school provides. If we have more time I will update this to actually include
#The actual majors each school provides.
majors = [1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39]
def generate_random_list_of_majors(majors_list):
	random.seed(datetime.now())
	random_values = random.sample(xrange(len(majors_list)), random.randint(1, len(majors_list)))
	result_list = []
	for value in random_values:
		result_list.append(majors_list[value])
	return result_list

db = client['nextsteps'] #selects 
user_coll = db.user
user_coll.remove()
user_file = open("sample_user.csv", "r")
user_list = list()
user_list = parse_file(user_file)
user_coll.insert(user_list)
user_file.close()
print("initializing DB")

school_coll = db.school
school_coll.remove()
school_file = open("ny_schools_v2.csv", "r")
#school_list = list()
school_list = parse_file(school_file)
#print(school_list)
for item in school_list:
	item['accepted_students'] = []
	item['MAJORS'] = generate_random_list_of_majors(majors)
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

print("done")
