from pymongo import MongoClient
from normalize_func import normalize
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.feature_extraction import DictVectorizer

client = MongoClient() #create connection to MongoDB
db = client['nextsteps'] #selects capstone database
user_coll = db.user 
school_coll = db.school
major_coll = db.major
degree_coll = db.degree
region_coll = db.region
state_coll = db.state
user_fit_coll = db.fit_user
school_fit_coll = db.fit_school
#school_fit_coll.remove()

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

def construct_training_model():
	vec = DictVectorizer()
	list_of_school = school_fit_coll.find({"UNITID": "480091"})
	for school in list_of_school:
		print(school)

	vector = vec.fit_transform(list_of_school)

	print(vector)

	'''regression = linear_model.LinearRegression()
	regression.fit(vec)

	plt.scatter(regression,  color='black')
	plt.plot(regression, color='blue', linewidth=3)
	plt.show()'''



# compare both to calculate user-school fit number


def main():
	print("hello - calculate the user's fit numbers")
	#calculate_school_fit_number()
	construct_training_model()




if __name__ == "__main__":
	main()