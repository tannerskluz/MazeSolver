from PIL import Image
import cv2
import numpy as np
import sys
from pathlib import Path
import preprocess as preprocess

def cv2_to_PIL(image):
	return Image.fromarray(image)

if __name__ == "__main__":
	#check that command line argument is taken in
	if len(sys.argv) < 2:
		print("How to run: \npython3 main.py ~~path_to_image~~")
		exit()
	image_path = sys.argv[1]
	print("input file: ", image_path)
	file_check = Path(image_path)

	#check that file exits
	if not file_check.is_file():
		print("File does not exist, terminating")
		exit()

	#returns preprocessed image in binary output form
	processed_bits = preprocess.regular_threshold(image_path)
	# view = cv2_to_PIL(processed_bits)
	# view.show()

