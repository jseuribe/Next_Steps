import csv

def parse_file(filename):
	header = []
	header_check = False
	info_list = list()

	for current_line in filename.readlines():
		current_line = current_line.strip() # remove whitespaces in lines
		if header_check == False:
			header_list = current_line.split(",")
			for each in header_list:
				header.append(each)
			header_check = True
		else:
			current = {}
			parts = current_line.split(",")
			for part, head in zip(parts, header):
				current[head] = part
			info_list.append(current)

	return(info_list)
