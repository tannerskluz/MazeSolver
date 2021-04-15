from Node import NodeBFS, NodeAStar
import cv2
from PIL import Image
import numpy as np
import time
from heapq import heappush, heappop


def regular_threshold(image_path: str):
	input_image = cv2.imread(image_path, 0)
	# input_image = cv2.medianBlur(input_image, 5)
	ret, binary_output = cv2.threshold(input_image, 127, 255, cv2.THRESH_BINARY)
	return binary_output


def heuristic(current_node, end_node):
	return abs(current_node.row - end_node.row) + abs(current_node.col - end_node.col)


class Maze:
	def __init__(self, image_path, start, end):
		self.image_path = image_path
		self.start_coordinate = start
		self.end_coordinate = end
		self.node_matrix = None
		self.solution_path = list()
		# open image and assign rest of variables
		self.image = cv2.imread(image_path, 1)
		self.processed_image = regular_threshold(self.image_path)
		if self.image.size == 0:
			print("Image not loaded correctly using openCV")
			exit(1)
		self.rows, self.cols, self.channels = self.image.shape
		self.bfs_mode = True

	def get_node_neighbors(self, node):
		neighbors = list()
		r, c = node.row, node.col
		if self.bfs_mode:
			if r > 0 and not self.node_matrix[r - 1][c].processed and not self.node_matrix[r - 1][c].condition == 0:
				neighbors.append(self.node_matrix[r - 1][c])
			if r < self.cols - 1 and not self.node_matrix[r + 1][c].processed and not self.node_matrix[r + 1][c].condition == 0:
				neighbors.append(self.node_matrix[r + 1][c])
			if c > 0 and not self.node_matrix[r][c - 1].processed and not self.node_matrix[r][c - 1].condition == 0:
				neighbors.append(self.node_matrix[r][c - 1])
			if c < self.rows - 1 and not self.node_matrix[r][c + 1].processed and not self.node_matrix[r][c + 1].condition == 0:
				neighbors.append(self.node_matrix[r][c + 1])
		else:
			if r > 0 and not self.node_matrix[r - 1][c].condition == 0:
				neighbors.append(self.node_matrix[r - 1][c])
			if r < self.cols - 1 and not self.node_matrix[r + 1][c].condition == 0:
				neighbors.append(self.node_matrix[r + 1][c])
			if c > 0 and not self.node_matrix[r][c - 1].condition == 0:
				neighbors.append(self.node_matrix[r][c - 1])
			if c < self.rows - 1 and not self.node_matrix[r][c + 1].condition == 0:
				neighbors.append(self.node_matrix[r][c + 1])
		print(len(neighbors))
		return neighbors

	def solve_bfs(self):
		self.bfs_init()
		duration, number_nodes_visited = self.find_path_bfs()
		return self.draw_path(), duration, number_nodes_visited

	def solve_a_star(self):
		self.a_star_init()
		duration, number_nodes_visited = self.find_path_a_star()
		return self.draw_path(), duration, number_nodes_visited

	def bfs_init(self):
		self.bfs_mode = True
		self.node_matrix = np.empty((self.rows, self.cols), dtype=object)
		for r in range(self.rows):
			for c in range(self.cols):
				self.node_matrix[r][c] = NodeBFS(c, r)
				self.node_matrix[r][c].condition = self.processed_image[r][c]
		self.node_matrix[self.end_coordinate[1]][self.end_coordinate[0]].condition = -2

	def a_star_init(self):
		self.bfs_mode = False
		self.node_matrix = np.empty((self.rows, self.cols), dtype=object)
		for r in range(self.rows):
			for c in range(self.cols):
				self.node_matrix[r][c] = NodeAStar(c, r)
				self.node_matrix[r][c].condition = self.processed_image[r][c]
		self.node_matrix[self.end_coordinate[1]][self.end_coordinate[0]].condition = -2

	def find_path_bfs(self):
		start_time = time.time()
		queue = list()
		queue.append(self.node_matrix[self.start_coordinate[1]][self.start_coordinate[0]])
		node_count = 1
		while len(queue) > 0:
			visiting_node = queue.pop(0)
			print(visiting_node.col, visiting_node.row)
			node_count += 1
			neighbors = self.get_node_neighbors(visiting_node)
			for neighbor_node in neighbors:
				neighbor_node.processed = True
				neighbor_node.parent_node = visiting_node
				if neighbor_node.condition != -2:
					queue.append(neighbor_node)
				else:
					print("BFS algorithm has found a solution path")
					self.solution_path = self.generate_path(neighbor_node)
					end_time = time.time()
					return (start_time - end_time), node_count
		end_time = time.time()
		print("BFS algorithm did not find a solution path")
		return (start_time - end_time), -1

	def find_path_a_star(self):
		start_time = time.time()
		start_node = self.node_matrix[self.start_coordinate[1]][self.start_coordinate[0]]
		start_node.g_score = 0
		end_node = self.node_matrix[self.end_coordinate[1]][self.end_coordinate[0]]
		start_node.f_score = heuristic(start_node, end_node)
		open_set = []
		heappush(open_set, start_node)
		node_count = 1
		while open_set:
			visiting_node = heappop(open_set)
			print(visiting_node.col, visiting_node.row)
			node_count += 1
			if visiting_node.condition != -2:
				visiting_node.out_open_set = True
				visiting_node.closed = False
				for neighbor in self.get_node_neighbors(visiting_node):
					if neighbor.closed:
						continue
					tentative_g_score = visiting_node.g_score + 1
					if tentative_g_score >= neighbor.g_score:
						continue
					neighbor.parent_node = visiting_node
					neighbor.g_score = tentative_g_score
					neighbor.f_score = neighbor.g_score + heuristic(neighbor, end_node)
					if neighbor.out_open_set:
						neighbor.out_open_set = False
						heappush(open_set, neighbor)
					else:
						open_set.remove(neighbor)
						heappush(open_set, neighbor)
			else:
				print("A* algorithm has found a solution path")
				self.solution_path = self.generate_path(visiting_node)
				end_time = time.time()
				return (start_time - end_time), node_count
		end_time = time.time()
		print("A* algorithm did not find a solution path")
		return (start_time - end_time), -1

	def generate_path(self, node):
		iter_node = node
		path = list()
		while iter_node.r != self.end_coordinate[1] or iter_node.c != self.end_coordinate[0]:
			path.append((iter_node.c, iter_node.r))
			iter_node = iter_node.parent_node
		return path

	def draw_path(self):
		path_pixels = 6
		circle_r = 6
		if max(self.rows, self.cols) >= 2000:
			path_pixels = 10
			circle_r = 10
		elif max(self.rows, self.cols) >= 1000:
			path_pixels = 8
			circle_r = 8
		print("drawing path")
		maze_image = self.image.copy()
		x0, y0 = self.solution_path[0]
		for node in self.solution_path[1:]:
			x1, y1 = node
			cv2.line(maze_image, (x0, y0), (x1, y1), (255, 0, 0), path_pixels)
			x0, y0 = node
		cv2.circle(maze_image, self.start_coordinate, circle_r, (0, 200, 40), -1)
		cv2.circle(maze_image, self.end_coordinate, circle_r, (0, 0, 255), -1)
		return Image.fromarray(maze_image)
