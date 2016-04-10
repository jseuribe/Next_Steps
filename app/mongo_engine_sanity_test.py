from mongoengine import *
#SANITY TEST
connect('test')

class User(Document):
	user_id = IntField(min_value=0, max_value=9001)

	def set(self, queryObj):
		user_id_vessel = IntField(min_value=0, max_value=9001)
		user_id_vessel = queryObj.user_id
		self.user_id = user_id_vessel

	@classmethod
	def cool_spot(self):
		print("Howdy!", self.user_id)


vessel = User.objects(user_id=612)

u = User()
if not vessel:
	print("no results found")
else:
	u = vessel[0]
	print(u.user_id)