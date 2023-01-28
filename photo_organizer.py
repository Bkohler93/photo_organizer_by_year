import os
import shutil
from datetime import datetime
import sys

# specify the path to the directory containing the photos
directory = '/Users/brettkohler/Pictures'

if len(sys.argv) == 2:
	directory = sys.argv[1]

def get_all_files(directory):
	all_files = []
	for root, _, files in os.walk(directory):
		for file in files:
			all_files.append(os.path.join(root, file))
	return all_files

def file_already_in_directory(file, directory):
	file_path = os.path.abspath(file)
	directory = os.path.abspath(directory)

	return os.path.commonprefix([file_path, directory]) == directory

# get a list of all files in the directory
files = get_all_files(directory)

if len(files) == 0:
	print("=== The directory you have provided is empty or does not exist")
	exit

# iterate through the list of files
for file in files:
	# check if the file is a photo (assumes jpeg file format)
	if file.endswith('.jpeg'):
		# get file path and directory
		filePath = os.path.join(directory, file)

		# get the file's creation time
		timestamp = os.path.getmtime(filePath)

		# convert the timestamp to a datetime object
		date = datetime.fromtimestamp(timestamp)

		# extract the year from the datetime object
		year = str(date.year)

		# get the path to the correct year directory and path to file
		yearDir = os.path.join(directory, year)

		# create a folder for the current year (if it doesn't already exist)
		if not os.path.exists(yearDir):
			os.makedirs(yearDir)
		elif file_already_in_directory(file, yearDir):
			# print(file + " already exists in directory\t" + yearDir)
			continue
			
		# move the file to the corresponding year folder
		shutil.move(filePath, yearDir)
