import pymongo
import random
from random import randint
from datetime import datetime
client = pymongo.MongoClient()

pym_db = client['nextsteps']

random.seed(datetime.now())
def pull_random_schools():#Basic function that returns some schools.
	return pym_db.school.find().limit(1).skip(int(randint(0,9))).next()

print(pull_random_schools())