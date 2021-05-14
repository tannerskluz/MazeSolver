from Maze import Maze
import sys
from pathlib import Path

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("How to run: \npython3 Main.py ~AlgorithmOption(A/B/AB)~ ~ShowPathOption(0/1)~ ~SaveOption(0/1)~ ~~path_to_image~~ ~xStart,yStart~ ~xEnd,yEnd~")
		print('Run Options:')
		print('A = A*')
		print('B = BFS')
		print('AB = both')
		exit()
	image_path = sys.argv[4]
	start = sys.argv[5]
	end = sys.argv[6]
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
		print("How to run: \npython3 Main.py ~AlgorithmOption(A/B/AB)~ ~ShowPathOption(0/1)~ ~SaveOption(0/1)~ ~~path_to_image~~ ~xStart,yStart~ ~xEnd,yEnd~")
		exit()

	save = False
	try:
		save_option = int(sys.argv[3])
		if save_option == 1:
			save = True
	except Exception:
		pass

	show_history_option = int(sys.argv[2])
	if show_history_option == 1:
		show_history = True
	else:
		show_history = False
	

	run_option = sys.argv[1]
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
	print("Start coordinate: (" + str(x_start) + ', ' + str(y_start) + ')')
	print("End coordinate: (" + str(x_end) + ', ' + str(y_end) + ')')
	file_check = Path(image_path)

	# check that file exits
	if not file_check.is_file():
		print("File does not exist, terminating")
		exit()

	print('-----------------------------')
	user_maze = Maze(image_path, (x_start, y_start), (x_end, y_end), show_history)

	if run_BFS:
		bfs_solution_image, bfs_duration, bfs_number_nodes = user_maze.solve_bfs()
		if bfs_number_nodes > 0:
			print(f'BFS algorithm found a solution in {bfs_duration:.3f} seconds')
			print(f'By visiting {bfs_number_nodes} nodes')
			if not save:
				bfs_solution_image.show()
			else:
				# save image
				save_path = 'maze_images/generated_solutions/' + image_path.split('/')[-1].split('.')[
					0] + '_solutionBFS.png'
				print(f'Saving image under: {save_path}')
				bfs_solution_image.save(save_path)
		print('-----------------------------')

	if run_a_star:
		a_star_solution_image, a_star_duration, a_star_number_nodes = user_maze.solve_a_star()
		if a_star_number_nodes > 0:
			print(f'A* algorithm found a solution in {a_star_duration:.3f} seconds')
			print(f'By visiting {a_star_number_nodes} nodes')
			if not save:
				a_star_solution_image.show()
			else:
				# save image
				save_path = 'maze_images/generated_solutions/' + image_path.split('/')[-1].split('.')[
					0] + '_solutionA*.png'
				print(f'Saving image under: {save_path}')
				a_star_solution_image.save(save_path)
		print('-----------------------------')
