from mongoengine import *
#SANITY TEST
connect('test')

class User(Document):
	user_id = IntField(min_value=0, max_value=9001)

#bobbert = User(user_id=413).save()

vessel = User.objects(user_id=2)

if not vessel:
	print("no results found")
else:
	for result in vessel:
		print(result.user_id)