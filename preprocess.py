from PIL import Image
import cv2
import sys

def cv2_to_PIL(image):
	return Image.fromarray(image)

def regular_threshold(image_path: str):
    input_image = cv2.imread(image_path, 0)
    # input_image = cv2.medianBlur(input_image, 5)
    ret, binary_output = cv2.threshold(input_image, 127, 255, cv2.THRESH_BINARY)
    return binary_output

