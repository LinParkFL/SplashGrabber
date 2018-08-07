import hashlib
from filter_and_save_images import get_files
from base64 import b64encode
from os import listdir, remove
from os.path import isfile, join

def remove_duplicate_images(image_paths):
	"""
	Returns a list of paths to unique images, excluding the duplicate images.
	Also removes the duplicated images from the given path.
	Args:
		image_paths (list[str]): List of paths to the images to compare.
	"""
	hashed_images_seen = {}
	
	for path in image_paths:
		with open(path, 'rb') as f:
			raw_image_data = f.read()
		
		encoded_data = b64encode(raw_image_data)
		
		# get the hash of this image
		hashed_image = hashlib.sha256(encoded_data).hexdigest()
		
		if hashed_image not in hashed_images_seen.values():
			# store the image in the dictionary if the image hasn't been seen yet
			hashed_images_seen[path] = hashed_image
		else:
			# remove this duplicated image from the folder
			remove(path)
			
	return hashed_images_seen.keys()

def main():
	path_to_saved_images = 'new_images'
	image_paths = get_files(path_to_saved_images)
	remove_duplicate_images(image_paths)

if __name__ == "__main__":
	main()
	
