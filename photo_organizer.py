import os
import shutil
from datetime import datetime
import sys

# specify the path to the directory containing the photos
directory = input('Enter the directory path where your photos are located within.\nFormatted like: /Users/brettkohler/Pictures\nDirectory path: ')
outDirectory = input('Enter the directory path where the photos will be placed\nDirectory path: ')

# get all files within a given directory recursively
def get_all_files(directory):
	all_files = []
	for root, _, files in os.walk(directory):
		for file in files:
			all_files.append(os.path.join(root, file))
	return all_files

# check if the file is already in current directory
def file_already_in_directory(file, directory):
	file_path = os.path.abspath(file)
	directory = os.path.abspath(directory)

	return os.path.commonprefix([file_path, directory]) == directory

# determine if file is an image
def file_is_image(file):
	return file.endswith('.jpeg') or file.endswith('.jpg') or file.endswith('.png')

def extract_file_name(path):
	return path[path.rfind('/') + 1:]

def extract_dir_path_from_file(path):
	return path[:path.rfind('/')]

# continue to edit file until the file would be unique within yearDir
def uniqify(file, yearDir):
		counter = 0
		
		# extract only file name without path
		file = extract_file_name(file)

		dotIdx = file.find('.')

		if file[dotIdx-2] == '_':
			dotIdx -= 1
			formatFileName = file[:dotIdx] + '{}' + file[dotIdx + 1:]
		else:
			formatFileName = file[:dotIdx] + '_{}' + file[dotIdx:]

		while os.path.isfile(os.path.join(yearDir, formatFileName.format(counter))):
			counter += 1
		formatFileName = formatFileName.format(counter)
		return formatFileName

def dir_empty(dir_path):
	return not any((True for _ in os.scandir(dir_path)))


# get a list of all files in the directory
files = get_all_files(directory)

if len(files) == 0:
	print("=== The directory you have provided is empty or does not exist")
	exit

# maintain count of files moved
count = 0

# iterate through the list of files
for file in files:

	# check if the file is a photo (assumes jpeg file format)
	if file.lower().endswith('.jpeg') or file.lower().endswith('.jpg') or file.lower().endswith('.png'):

		# get full file path
		filePath = os.path.join(directory, file)

		# get the file's creation time
		try:
			timestamp = os.path.getmtime(filePath)
		except:
			print("Error, skipping on from line 75 :(")
			continue

		# convert the timestamp to a datetime object
		date = datetime.fromtimestamp(timestamp)

		# extract the year from the datetime object
		year = str(date.year)

		# get the path to the correct year directory and path to file
		yearDir = os.path.join(outDirectory, year)

		# create outDirectory if not created
		if not os.path.exists(outDirectory):
			try:
				os.makedirs(outDirectory)
			except:
				print("Failed to create output directory, check to make sure you entered the correct directory name")
				exit()

		# create a folder for the current year (if it doesn't already exist)
		if not os.path.exists(yearDir):
			os.makedirs(yearDir)

		# move to next file if current file already in correct directory	
		if file_already_in_directory(file, yearDir):
			continue
		
		# create file path that matches new year directory
		filePathYearDir = os.path.join(yearDir, file)

		#
		isChanged = False

		# append number if a copy exists with same name in yearDir
		if os.path.isfile(filePathYearDir):
			try:
				isChanged = True

				# create new file name with appended number to make it unique to other copies
				uniqueFilePath = os.path.join(directory, uniqify(file, yearDir))
				os.rename(filePath, uniqueFilePath)

				# rename file to new unique file path
				shutil.move(uniqueFilePath, yearDir)
			except:
				print("Error, skipping file from line 96-99 :(")
				continue
		else:
			# change modified date to 'date' saved above
			shutil.move(filePath, yearDir)

		# increment counter
		count += 1

		# extract directory without filename
		dir = extract_dir_path_from_file(file)

		# if directory of current file is now empty delete it
		if dir_empty(dir):
			os.rmdir(dir)
			

print("Done: Moved " + str(count) + " images")