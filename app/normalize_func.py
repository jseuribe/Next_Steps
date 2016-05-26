from __future__ import division
import numpy as np

'''
Helper functions for algorithm_main
'''

# x passes in the name and value of the normalized value
# coll passes in the collection where to find x
def normalize(name, value, coll):
	if str(value) not in "NULL":
		list_of_all_possible_values = coll.find({}, {name: 1})
		value_list = []

		for item in list_of_all_possible_values:
			#print(item[name])
			if str(item[name]) not in "NULL": 
				value_list.append(item[name])

		#value_list.remove(unicode("NULL"))

		max_value = int(max(value_list))
		min_value = int(min(value_list))
		'''print("Printing values")
		print(max_value)
		print(min_value)
		print(value)'''

		normalized_num = int(value)-min_value
		normalized_den = max_value-min_value

		return (normalized_num/normalized_den)
	else:
		return None