from pymongo import MongoClient
from normalize_func import normalize

client = MongoClient() #create connection to MongoDB
db = client['capstone'] #selects capstone database
user_coll = db.user 
school_coll = db.school
major_coll = db.major
degree_coll = db.degree
region_coll = db.region
state_coll = db.state



def main():
	x = ("SAT_read", 687)
	print(normalize(x, user_coll))


if __name__ == "__main__":
	main()