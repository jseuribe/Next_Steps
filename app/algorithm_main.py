from __future__ import division, print_function
from pymongo import MongoClient
from normalize_func import normalize
#import matplotlib.pyplot as plt
import numpy as np
#from sklearn import linear_model
#from sklearn.feature_extraction import DictVectorizer
import pprint

client = MongoClient() #create connection to MongoDB
db = client['nextsteps'] #selects capstone database
user_coll = db.user 
school_coll = db.school
major_coll = db.major
degree_coll = db.degree
region_coll = db.region
state_coll = db.state

pp = pprint.PrettyPrinter(indent=4)

ADMISSION_RATE_MAX = 100
ADMISSION_RATE_MIN = 0
ADMISSION_RATE_MAX = 100
ADMISSION_RATE_MIN = 0
GENERAL_PREFERENCE_VALUE = 5
STUDENT_DEBT_MAX = 500000
STUDENT_DEBT_MIN = 0

# Calculate fit number for users
'''#username,f_name,m_name,l_name,email,state,gpa,tuition,cost_preference,degree,academic_preference,distance_preference,dorm_price,SAT_math,SAT_read,SAT_write
def calculate_users_fit_number():
	for user in user_coll.find():
		gpa_fit = normalize(("gpa", int(user["gpa"])), user_coll)
		 m
		#print(user["username"], value)
'''
# calculate fit number for schools
'''def calculate_school_fit_number():
	for attribute in school_coll.find():
		cost = normalize("COSTT4A", attribute["COSTT4A"], school_coll)
		sat_verbal = normalize("SATVRMID", attribute["SATVRMID"], school_coll)
		sat_math = normalize("SATMTMID", attribute["SATMTMID"], school_coll)
		sat_writing = normalize("SATWRMID", attribute["SATWRMID"], school_coll)
		highest_degree = normalize("HIGHDEG", attribute["HIGHDEG"], school_coll)
		to_insert = {"type": "school","UNITID": attribute["UNITID"], "admissions_rate": attribute["ADM_RATE"], "norm_cost": cost, "norm_sat_verbal": sat_verbal, "norm_sat_math": sat_math, "norm_sat_writing": sat_writing, "norm_highest_degree": highest_degree}
		school_fit_coll.insert_one(to_insert)'''
'''def construct_training_model():
	vec = DictVectorizer()
	list_of_school = school_fit_coll.find({"UNITID": "480091"})
	for school in list_of_school:
		print(school)

	vector = vec.fit_transform(list_of_school)

	print(vector)

	regression = linear_model.LinearRegression()
	regression.fit(vec)

	plt.scatter(regression,  color='black')
	plt.plot(regression, color='blue', linewidth=3)
	plt.show()'''
# compare both to calculate user-school fit number

def extract_this_attribute(user_collection, attribute, username):
	print('EXTRACTED ATTRIBUTE=======================================')
	value_cursor = user_collection.find({'username': username}, {attribute: 1, '_id': 0})
	value = None
	for record in value_cursor:
		print('EXTRACTED ATTRIBUTE=======================================')
		print(record[attribute])
		value = record[attribute]
	return value

def displayEveryFitSchools():
	# Recalculate all Fit-Numbers
	calculateAllFitNumbers()

	for user in user_coll.find():
		pp.pprint(user)


def calculateAllFitNumbers():
	user_coll.update({}, {'$unset':{"recommended_schools": 1}}, multi= True)
	for student in user_coll.find():
		for school in school_coll.find():
			fit_number = calculateFitNumber(student, school)
			string_id = "recommended_schools." + school["INSTNM"]
			user_coll.update_one({"_id": student["_id"]}, {'$set':{string_id: fit_number}})

def getPredictedAcceptedValue(key, school):
	predicted_value = 0.0
	size = len(list(school["accepted_students"]))
	print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa')
	print(school['accepted_students'])
	if (key == "SAT_read"):
		if (school["SATVRMID"] != "NULL"):
			predicted_value = int(school["SATVRMID"])
		if school["accepted_students"]:
			for each_accepted_students in school["accepted_students"]:
				predicted_value += int(extract_this_attribute(user_coll, 'SAT_read', each_accepted_students))
	elif (key == "SAT_math"):
		if (school["SATMTMID"] != "NULL"):
			predicted_value = int(school["SATMTMID"])
		if school["accepted_students"]:
			for each_accepted_students in school["accepted_students"]:
				predicted_value += int(extract_this_attribute(user_coll, 'SAT_math', each_accepted_students))
	elif (key == "SAT_write"):
		if (school["SATWRMID"] != "NULL"):
			predicted_value = int(school["SATWRMID"])
		if school["accepted_students"]:
			for each_accepted_students in school["accepted_students"]:
				predicted_value += int(extract_this_attribute(user_coll, 'SAT_write', each_accepted_students))
	elif (key == "ACT_English"):
		if (school["ACTENMID"] != "NULL"):
			predicted_value = int(school["ACTENMID"])
		if school["accepted_students"]:
			for each_accepted_students in school["accepted_students"]:
				predicted_value += int(extract_this_attribute(user_coll, 'ACT_English', each_accepted_students))
	elif (key == "ACT_Math"):
		if (school["ACTMTMID"] != "NULL"):
			predicted_value = int(school["ACTMTMID"])
		if school["accepted_students"]:
			for each_accepted_students in school["accepted_students"]:
				predicted_value += int(extract_this_attribute(user_coll, 'ACT_Math', each_accepted_students))
	elif (key == "ACT_Reading"):
		if (school["ACTWRMID"] != "NULL"):
			predicted_value = int(school["ACTWRMID"])
		if school["accepted_students"]:
			for each_accepted_students in school["accepted_students"]:
				predicted_value += int(extract_this_attribute(user_coll, 'ACT_Reading', each_accepted_students))
	elif (key == "gpa"):
		sum = 0
		for each_accepted_students in school["accepted_students"]:
			print('HELLLLLLLLLOOOOOOOOOOOO')
			print("--------Extracting Attribute----------------------------: ")

			sum += int(extract_this_attribute(user_coll, 'gpa', each_accepted_students))
		predicted_value = sum
	
	# Gets the average of all of the accepted student's value.
	predicted_value = predicted_value/(size + 1)
	#print(predicted_value)
	return predicted_value



def calculateFitNumber(student, school):
	############## Important Items ##############

	# Check degree preference
	pref_d_val = 0
	d_pref_string = student[u"pref_degree"]
	if isinstance(d_pref_string, str):
		pref_d_val = 0
	else:
		pref_d_val = student[u'pref_degree']
	if (pref_d_val != 0):
		# If the student's preferred degree is greater than the school's highest awarded degree
		if (int(pref_d_val) > int(school["HIGHDEG"])):
			return -100
	#this now correlates to the user objects generated by the setup phase

	############## General Items ##############

	general_value = 0.0
	general_changes = 0.0

	# Check admissions rate. If the rate is above average, increment value.
	if (school["ADM_RATE"] != "NULL") and (float(school["ADM_RATE"]) < (ADMISSION_RATE_MAX+ADMISSION_RATE_MIN)/200.0):
		general_value += 1
	general_changes += 1

	# Check transfer rate
	if (school["WDRAW_ORIG_YR2_RT"] != "NULL") and (float(school["WDRAW_ORIG_YR2_RT"]) < (TRANSFER_RATE_MAX+TRANSFER_RATE_MIN)/200.0):
		general_value += 1
	general_changes += 1

	# Check degrees offered - if it awards Bachelors and and above 
	if (int(school["PREDDEG"]) >= 3):
		general_value += 1
		general_changes += 1

	# Check majors - school offers perfered major of the student's
	for pref_major in student["major_preference_list"]:
		if pref_major not in "NO_PREFERENCE":
			if major_coll.find({"smid": pref_major}):
				general_value += 1
				general_changes += 1

	# Fit number for general items
	general_fit_number = general_value/general_changes * 100.0
	

	############## Distance ##############

	distance_value = 0.0
	distance_changes = 0.0

	# Check users' preferred state
	for pref_state in student["state_preference_list"]:
		if pref_state == school["st_fips"]:
			distance_value += 1
			distance_changes += 1

	# Fit number for distance 
	distance_fit_number = 0
	if (distance_value != 0):
		distance_fit_number = (distance_value/distance_changes) * 100.0

	############## Academics ##############

	academic_value = 0
	academic_changes = 0

	# Check grades
	if (student["gpa"] >= getPredictedAcceptedValue("gpa", school)):
		academic_value += 1
	else:
		academic_value -= 1
	academic_changes += 1

	# Check ACT English
	if (student["ACT_English"] >= getPredictedAcceptedValue("ACT_English", school)):
		academic_value += 1
	else:
		academic_value -= 1
	academic_changes += 1

	# Check ACT Math
	if (student["ACT_Math"] >= getPredictedAcceptedValue("ACT_Math", school)):
		academic_value += 1
	else:
		academic_value -= 1
	academic_changes += 1

	# Check ACT Writing/ Reading
	if (student["ACT_Reading"] >= getPredictedAcceptedValue("ACT_Reading", school)):
		academic_value += 1
	else:
		academic_value -= 1
	academic_changes += 1

	# Check SAT English
	if (student["SAT_read"] >= getPredictedAcceptedValue("SAT_read", school)):
		academic_value += 1
	else:
		academic_value -= 1
	academic_changes += 1

	# Check SAT Math
	if (student["SAT_math"] >= getPredictedAcceptedValue("SAT_math", school)):
		academic_value += 1
	else:
		academic_value -= 1
	academic_changes += 1

	# Check SAT Writing
	if (student["SAT_write"] >= getPredictedAcceptedValue("SAT_write", school)):
		academic_value += 1
	else:
		academic_value -= 1
	academic_changes += 1

	# Fit number for academic
	academic_fit_number = 0
	if (academic_value != 0):
		academic_fit_number = academic_value/academic_changes * 100.0


	############## Cost ##############
	cost_value = 0
	cost_changes = 0

	# Check average student debt
	if not 'GRAD_DEBT_MDN' in school:
		pass
	elif (school["GRAD_DEBT_MDN"] < (STUDENT_DEBT_MAX+STUDENT_DEBT_MIN)/2.0):
		cost_value += 1
	elif (school["GRAD_DEBT_MDN"] == "NULL"):
		pass
	else:
		cost_value -= 1
	cost_changes += 1

	# Check tuition
	if (student["tuition"] < school["COSTT4A"]):
		cost_value += 1
	elif (school["COSTT4A"] == "NULL"):
		pass
	else:
		cost_value -= 1
	cost_changes +=1

	# Fit number for cost
	cost_fit_number = cost_value/cost_changes * 100.0

	# Calculate preferences
	total_preferences = GENERAL_PREFERENCE_VALUE + int(student["distance_preference"]) + int(student["academic_preference"]) + int(student["cost_preference"])
	general_preference = GENERAL_PREFERENCE_VALUE / total_preferences
	distance_preference = int(student["distance_preference"]) / total_preferences
	academic_preference = int(student["academic_preference"]) / total_preferences
	cost_preference = int(student["cost_preference"]) / total_preferences

	# Calculate the Final Fit Number
	total_fit_number = (general_fit_number * general_preference) + (distance_fit_number * distance_preference) + (academic_fit_number * academic_preference) + (cost_fit_number * cost_preference)

	return total_fit_number

def run_fit():
	#school_coll.update({}, {'$set':{"accepted_students": {}}}, multi=True)
	#calculate_school_fit_number()
	#construct_training_model()
	print("this takes a while, please hold")
	displayEveryFitSchools()



#if __name__ == "__main__":
#	main()