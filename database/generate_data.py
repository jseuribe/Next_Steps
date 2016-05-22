import random
import testdata

class Users(testdata.DictFactory):
	SAT_math = testdata.RandomInteger(200, 800) 
	SAT_read = testdata.RandomInteger(200, 800) 
	SAT_write = testdata.RandomInteger(200, 800) 
	academic_preference = testdata.RandomInteger(1, 5) 
	cost_preference = testdata.RandomInteger(1, 5) 
	degree = testdata.RandomSelection(['Associate', 'Bachelor', 'Master', 'No Preference'])
	distance_preference = testdata.RandomInteger(1, 5) 
	dorm_price = random.choice([5000, 10000, 15000, 20000])
	email = testdata.FakeDataFactory('email')
	f_name = testdata.FakeDataFactory('firstName')
	gpa = testdata.RandomInteger(65, 100)
	l_name = testdata.FakeDataFactory('lastName')
	address = testdata.FakeDataFactory('address')
	tuition = random.choice([5000, 10000, 20000, 30000, 50000, 100000])

f = open("sample_user_2.txt", 'w')
for user in Users().generate(10):
	user["username"] = user["email"]
	print (user)
	f.write(user+',')
f.close()
