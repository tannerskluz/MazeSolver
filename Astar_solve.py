import numpy as np
from Vertex import Vertex
from heapq import heappush, heappop


def get_neighbors(mat, r, c):
	shape = mat.shape
	neighbors = []
	# ensure neighbors are within image boundaries
	if r > 0 and not mat[r - 1][c].processed and not mat[r - 1][c].condition == 0:
		neighbors.append(mat[r - 1][c])
	if r < shape[0] - 1 and not mat[r + 1][c].processed and not mat[r + 1][c].condition == 0:
		neighbors.append(mat[r + 1][c])
	if c > 0 and not mat[r][c - 1].processed and not mat[r][c - 1].condition == 0:
		neighbors.append(mat[r][c - 1])
	if c < shape[1] - 1 and not mat[r][c + 1].processed and not mat[r][c + 1].condition == 0:
		neighbors.append(mat[r][c + 1])
	return neighbors


def heuristic(current_vertex, end_vertex):
	return abs(current_vertex.x - end_vertex.x) + abs(current_vertex.y - end_vertex.y)


def find_shortest_path_astar(matrix, x_start, y_start, x_end, y_end):
	lenrows, lencols = matrix.shape
	print('rows', lenrows)
	print('cols', lencols)
	vectorMatrix = np.empty((lenrows, lencols), dtype=object)
	for r in range(lenrows):
		for c in range(lencols):
			# print(matrix[0][0])
			vectorMatrix[r][c] = Vertex(c, r)
			vectorMatrix[r][c].condition = matrix[r][c]
	# vectorMatrix[y_start][x_start].condition = -1
	vectorMatrix[y_end][x_end].condition = -2
	start_vertex = vectorMatrix[y_start][x_start]
	start_vertex.gscore = 0
	end_vertex = vectorMatrix[y_end][x_end]
	start_vertex.fscore = heuristic(start_vertex, end_vertex)
	openSet = []
	heappush(openSet, start_vertex)
	nodeCount = 1
	while openSet:
		current = heappop(openSet)
		nodeCount += 1
		if current.condition == -2:
			print('found')
			path = []
			iter_v = current
			path.append((x_end, y_end))
			while (iter_v.y != y_start or iter_v.x != x_start):
				path.append((iter_v.x, iter_v.y))
				# print(iter_v.xParent)
				# print(iter_v.yParent)
				iter_v = vectorMatrix[iter_v.yParent][iter_v.xParent]
				# print('itertype2')
				# print(type(iter_v))
				# print('test2')
			return path, nodeCount
		current.out_openset = True
		current.closed = False
		for neighbor in get_neighbors(vectorMatrix, current.y, current.x):
			if neighbor.closed:
				continue
			tentative_gscore = current.gscore + 1
			if tentative_gscore >= neighbor.gscore:
				continue
			neighbor.xParent = current.x
			neighbor.yParent = current.y
			neighbor.gscore = tentative_gscore
			neighbor.fscore = neighbor.gscore + heuristic(neighbor, end_vertex)
			if neighbor.out_openset:
				neighbor.out_openset = False
				heappush(openSet, neighbor)
			else:
				openSet.remove(neighbor)
				heappush(openSet, neighbor)

	print('not found')
	return None, nodeCount
