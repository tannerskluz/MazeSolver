from PIL import Image
import cv2
import sys
import time
from pathlib import Path
import preprocess as preprocess
import bfs_solve as bfs
import Astar_solve as Astar


def cv2_to_pil(image):
	return Image.fromarray(image)


# path is list of tuples
def draw_path(img, path, thickness=5):
	# hello
	print('drawing path')
	x0, y0 = path[0]
	for vertex in path[1:]:
		# print(vertex)
		x1, y1 = vertex
		cv2.line(img, (x0, y0), (x1, y1), (255, 0, 0), thickness)
		x0, y0 = vertex


if __name__ == "__main__":
	# check that command line argument is taken in
	if len(sys.argv) < 4:
		print(
			"How to run: \npython3 main.py ~~path_to_image~~ ~xStart,yStart~ ~xEnd,yEnd~ ~Run Option~ ~DebugOption(0/1)~")
		print('Run Options:')
		print('A = A*')
		print('B = BFS')
		print('AB = both')
		exit()
	image_path = sys.argv[1]
	start = sys.argv[2]
	end = sys.argv[3]
	x_start = 0
	y_start = 0
	x_end = 0
	y_end = 0
	try:
		x_start = int((start.split(','))[0])
		y_start = int((start.split(','))[1])
		x_end = int((end.split(','))[0])
		y_end = int((end.split(','))[1])
	except Exception:
		print("How to run: \npython3 main.py ~~path_to_image~~ ~xstart,ystart~ ~xend,yend~")
		exit()

	debug = False
	try:
		debug_option = int(sys.argv[5])
		if debug_option == 1:
			debug = True
	except Exception:
		pass

	runOption = sys.argv[4]
	runAstar = False
	runBFS = False
	if 'A' in runOption:
		runAstar = True
	if 'B' in runOption:
		runBFS = True
	runBoth = runAstar and runBFS

	if runBoth:
		print('Running both BFS and A*')
	elif runAstar:
		print('Running A*')
	elif runBFS:
		print('Running BFS')
	else:
		print('Incorrect run option\nTerminating')
		exit(0)

	print("Input file: ", image_path)
	if debug:
		print("Start coordinate: (" + str(x_start) + ', ' + str(y_start) + ')')
		print("End coordinate: (" + str(x_end) + ', ' + str(y_end) + ')')
	file_check = Path(image_path)

	# check that file exits
	if not file_check.is_file():
		print("File does not exist, terminating")
		exit()

	image_array_color_BFS = cv2.imread(image_path, 1)
	image_array_color_Astar = cv2.imread(image_path, 1)
	height, width, channels = image_array_color_BFS.shape
	if debug:
		print("Image dimensions: (" + str(width) + ', ' + str(height) + ')')

	processed_bits = preprocess.regular_threshold(image_path)

	path_pixels = 6
	circle_r = 6
	if max(height, width) >= 2000:
		path_pixels = 10
		circle_r = 10
	elif max(height, width) >= 1000:
		path_pixels = 8
		circle_r = 8

	if debug:
		print('Path pixels: ', path_pixels)
		print('Circle pixels: ', circle_r)

	if runBFS:
		start_time_BFS = time.time()
		solve_path_BFS, nodesVisited = bfs.find_shortest_path_bfs(processed_bits, x_start, y_start, x_end, y_end)
		end_time_BFS = time.time()

		print('BFS solution found in ' + str(end_time_BFS - start_time_BFS) + ' seconds')
		print('Algorithm visisted ', nodesVisited, ' nodes')

		draw_path(image_array_color_BFS, solve_path_BFS, path_pixels)
		cv2.circle(image_array_color_BFS, (x_start, y_start), circle_r, (0, 200, 40), -1)
		cv2.circle(image_array_color_BFS, (x_end, y_end), circle_r, (0, 0, 255), -1)

		maze_w_solution_BFS = cv2_to_pil(image_array_color_BFS)

		if debug:
			maze_w_solution_BFS.show()
		else:
			# save image
			save_path = 'maze_images/generated_solutions/' + image_path.split('/')[-1].split('.')[
				0] + '_solutionBFS.png'
			print("Saving image under: ", save_path)
			maze_w_solution_BFS.save(save_path)

	if runAstar:
		start_time_Astar = time.time()
		solve_path_Astar, nodesVisited = Astar.find_shortest_path_astar(processed_bits, x_start, y_start, x_end, y_end)
		end_time_Astar = time.time()

		print('A* solution found in ' + str(end_time_Astar - start_time_Astar) + ' seconds')
		print('Algorithm visited ', nodesVisited, ' nodes')

		draw_path(image_array_color_Astar, solve_path_Astar, path_pixels)
		cv2.circle(image_array_color_Astar, (x_start, y_start), circle_r, (0, 200, 40), -1)
		cv2.circle(image_array_color_Astar, (x_end, y_end), circle_r, (0, 0, 255), -1)

		maze_w_solution_Astar = cv2_to_pil(image_array_color_Astar)

		if debug:
			maze_w_solution_Astar.show()
		else:
			# save image
			save_path = 'maze_images/generated_solutions/' + image_path.split('/')[-1].split('.')[
				0] + '_solutionAstar.png'
			print("Saving image under: ", save_path)
			maze_w_solution_Astar.save(save_path)
