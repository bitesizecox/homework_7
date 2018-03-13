# 507/206 Homework 7 Part 2
import json
# With the directory_dict.json you have in part 1, 
# this program should search the data you crawl to 
# find the number of PhD students in the directory.

count = 0
#### Your Part 2 solution goes here ####
umsi_file = open("directory_dict.json")
umsi_data = json.load(umsi_file)
for i in umsi_data.items():
	# print(i[1]['title'])
	if i[1]['title'] == "PhD student":
		count += 1
umsi_file.close()
#### Your answer output (change the value in the variable, count)####
print('The number of PhD students: ', count)
