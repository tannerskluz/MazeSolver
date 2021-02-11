from PIL import Image
import cv2
import numpy as np
import sys
from pathlib import Path
import preprocess as preprocess
import bfs_solve as bfs

def cv2_to_PIL(image):
	return Image.fromarray(image)

#path is list of tuples
def draw_path(img, path, thickness=5):
    print('drawing path')
    x0,y0=path[0]
    for vertex in path[1:]:
        #print(vertex)
        x1,y1=vertex
        cv2.line(img,(x0,y0),(x1,y1),(255,0,0),thickness)
        x0,y0=vertex

if __name__ == "__main__":
	#check that command line argument is taken in
	if len(sys.argv) < 4:
		print("How to run: \npython3 main.py ~~path_to_image~~ ~xstart,ystart~ ~xend,yend~")
		exit()
	image_path = sys.argv[1]
	start = sys.argv[2]
	end = sys.argv[3]
	try:
		x_start = int((start.split(','))[0])
		y_start = int((start.split(','))[1])
		x_end = int((end.split(','))[0])
		y_end = int((end.split(','))[1])
	except:
		print("How to run: \npython3 main.py ~~path_to_image~~ ~xstart,ystart~ ~xend,yend~")
		exit()

	print("Input file: ", image_path)
	print("Start coordinate: (" + str(x_start) + ', ' + str(y_start) + ')')
	print("End coordinate: (" + str(x_end) + ', ' + str(y_end) + ')')
	file_check = Path(image_path)

	#check that file exits
	if not file_check.is_file():
		print("File does not exist, terminating")
		exit()

	image_array_color = cv2.imread(image_path,1)
	height, width, channels = image_array_color.shape
	#cv2_to_PIL(image_array_color).show()

	#returns preprocessed image in binary output form
	processed_bits = preprocess.regular_threshold(image_path)
	# view = cv2_to_PIL(processed_bits)
	# view.show()

	path_pixels = 6
	circle_r = 6
	if max(height, width) >= 2000:
		path_pixels = 10
		circle_r = 10
	elif max(height, width) >= 1000:
		path_pixels = 8
		circle_r = 8


	solve_path = bfs.find_shortest_path_bfs(processed_bits, x_start, y_start, x_end, y_end)
	draw_path(image_array_color, solve_path, path_pixels)
	cv2.circle(image_array_color, (x_start, y_start), circle_r, (0,200,40), -1)
	cv2.circle(image_array_color, (x_end, y_end), circle_r, (0,0,255), -1)

	maze_w_solution = cv2_to_PIL(image_array_color)
	# maze_w_solution.show()

	#save image
	save_path = 'maze_images/generated_solutions/' + image_path.split('/')[-1].split('.')[0] + '_solution.png'
	print("Saving image under: ", save_path)
	maze_w_solution.save(save_path)

