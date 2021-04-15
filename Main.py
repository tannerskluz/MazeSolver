from Maze import Maze
import sys
from pathlib import Path

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("How to run: \npython3 main.py ~~path_to_image~~ ~xStart,yStart~ ~xEnd,yEnd~ ~Run Option~ ~DebugOption(0/1)~")
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
		print("How to run: \npython3 main.py ~~path_to_image~~ ~x_start,y_start~ ~x_end,y_end~")
		exit()

	debug = False
	try:
		debug_option = int(sys.argv[5])
		if debug_option == 1:
			debug = True
	except Exception:
		pass

	run_option = sys.argv[4]
	run_a_star = False
	run_BFS = False
	if 'A' in run_option:
		run_a_star = True
	if 'B' in run_option:
		run_BFS = True
	run_both = run_a_star and run_BFS

	if run_both:
		print('Running both BFS and A*')
	elif run_a_star:
		print('Running A*')
	elif run_BFS:
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

	user_maze = Maze(image_path, (x_start, y_start), (x_end, y_end))

	if run_BFS:
		bfs_solution_image, bfs_duration, bfs_number_nodes = user_maze.solve_bfs()
		if debug:
			bfs_solution_image.show()
		else:
			# save image
			save_path = 'maze_images/generated_solutions/' + image_path.split('/')[-1].split('.')[
				0] + '_solutionBFS.png'
			print("Saving image under: ", save_path)
			bfs_solution_image.save(save_path)

	if run_a_star:
		a_star_solution_image, a_star_duration, a_star_number_nodes = user_maze.solve_a_star()
		if debug:
			a_star_solution_image.show()
		else:
			# save image
			save_path = 'maze_images/generated_solutions/' + image_path.split('/')[-1].split('.')[
				0] + '_solutionA*.png'
			print("Saving image under: ", save_path)
			a_star_duration.save(save_path)
