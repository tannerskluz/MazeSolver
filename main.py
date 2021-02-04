from PIL import Image
import cv2
import numpy as np
import sys
from pathlib import Path
import preprocess as preprocess
import bfs_solve as bfs

def cv2_to_PIL(image):
	return Image.fromarray(image)

def draw_path(img,path, thickness=2):
    '''path is a list of (x,y) tuples'''
    print('drawing path')
    x0,y0=path[0]
    for vertex in path[1:]:
        #print(vertex)
        x1,y1=vertex
        cv2.line(img,(x0,y0),(x1,y1),(0,0,255),thickness)
        x0,y0=vertex

if __name__ == "__main__":
	#check that command line argument is taken in
	if len(sys.argv) < 6:
		print("How to run: \npython3 main.py ~~path_to_image~~ ~xstart~ ~ystart~ ~xend~ ~yend~")
		exit()
	image_path = sys.argv[1]
	x_start = int(sys.argv[2])
	y_start = int(sys.argv[3])
	x_end = int(sys.argv[4])
	y_end = int(sys.argv[5])
	print("Input file: ", image_path)
	print("Start: (" + str(x_start) + ', ' + str(y_start) + ')')
	print("Start: (" + str(x_end) + ', ' + str(y_end) + ')')
	file_check = Path(image_path)

	#check that file exits
	if not file_check.is_file():
		print("File does not exist, terminating")
		exit()

	image_array_color = cv2.imread(image_path,1)

	#returns preprocessed image in binary output form
	processed_bits = preprocess.regular_threshold(image_path)
	# view = cv2_to_PIL(processed_bits)
	# view.show()

	solve_path = bfs.find_shortest_path_bfs(processed_bits, x_start, y_start, x_end, y_end)
	draw_path(image_array_color, solve_path, 6)
	cv2.circle(image_array_color, (x_start, y_start), 5, (0,200,40), -1)
	cv2.circle(image_array_color, (x_end, y_end), 5, (255,0,0), -1)

	maze_w_solution = cv2_to_PIL(image_array_color)
	maze_w_solution.show()
