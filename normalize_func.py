from __future__ import division
import numpy as np


# x passes in the name and value of the normalized value
# coll passes in the collection where to find x
def normalize(x, coll):
	print("hello")
	list_of_all_possible_values = coll.find({}, {x[0]:1})
	value_list = []

	for item in list_of_all_possible_values:
		print(item[x[0]])
		value_list.append(int(item[x[0]]))

	max_value = max(value_list)
	min_value = min(value_list)
	print(max_value)
	print(min_value)
	print(x[1])

	normalized_num = x[1]-min_value
	normalized_den = max_value-min_value

	return (normalized_num/normalized_den)