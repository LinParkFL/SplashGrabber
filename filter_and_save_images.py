import ctypes
import get_image_size
from os import listdir
from os.path import isfile, join, getctime, getmtime
from time import gmtime, asctime, time
from shutil import copyfile

def get_files(path):
	"""
	Returns a list of paths to files in the given directory path.
	Args:
		path (str): The path to the directory where it will look for files in.
	"""
	files = []

	for f in listdir(path):
		tmpPath = join(path, f)
		
		# select only files, ignore folders
		if isfile(tmpPath):
			files.append(tmpPath)

	return files

def modified_within_x_days(path_to_file, num_days=1):
	"""
	Returns True if the file was modified within the given number of days.
			False otherwise.
	Args:
		path_to_file (str): The path to the file.
		num_days (int):	The maximum number of days since a file can be modified.
	"""
	curr_time = time()
	seconds_in_a_day = 3600 * 24 * num_days
	modified_time = getmtime(path_to_file)
	
	return modified_time >= curr_time - seconds_in_a_day

def is_img_right_size(path_to_file, min_width, min_height):
	"""
	Returns True if the image is screen size.
	Args:
		path_to_file (str): The path to the file.
		min_width (int): The minimum number of pixels that the width of the image has to be.
		min_height (int): The minimum number of pixels that the height of the image has to be.
	"""
	try:
		img = get_image_size.get_image_metadata(path_to_file)
		width, height = img.width, img.height
	except get_image_size.UnknownImageFormat:
		# this is probably not an image
		width, height = -1, -1
	
	return width >= min_width and height >= min_height

def filter_and_save_images(paths_to_files, new_directory, num_days=1, min_width=1920, min_height=1080):
	"""
	Returns nothing.
	Chooses the images that were modified within the past num_days days and that are screen sized.
	Moves the filtered images to the given directory.
	Args:
		paths_to_files (list[str]): List of paths to files.
		new_directory (str): The path to the directory where the images should be saved.
		num_days (int): The maximum number of days since a file can be modified to be considered.
		min_width (int): The minimum number of pixels that the width of the image has to be.
		min_height (int): The minimum number of pixels that the height of the image has to be.
	"""
	for f in paths_to_files:
		# filter for files that were modified in the last 24 hours
		if modified_within_x_days(f, num_days):
			# filter for images that are the same size (or bigger) than the screen
			if is_img_right_size(f, min_width, min_height):
				move_image_to_saved(f, new_directory)
				
def move_image_to_saved(path_to_file, new_directory):
	"""
	Returns nothing.
	"""
	image_name = path_to_file.split('\\')[-1] + '.jpg'
	new_path = join(new_directory, image_name)
	
	# copies the image to another folder, replaces file when necessary
	copyfile(path_to_file, new_path)
	
def main():
	# path to get splash screen images
	path_to_splash_screens = 'C:/Users/AdLin/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets'
	
	# path to move filtered images to
	new_path_to_saved_images = 'C:/Users/AdLin/Pictures/Spotlight'
	
	max_num_days_since_modified = 1
	
	# get the resolution of the device
	user32 = ctypes.windll.user32
	min_width, min_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
	
	files = get_files(path_to_splash_screens)
	filter_and_save_images(files, new_path_to_saved_images, max_num_days_since_modified, min_width, min_height)
	
if __name__ == '__main__':
	main()
