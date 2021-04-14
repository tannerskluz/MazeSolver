import numpy as np
from Vertex import Vertex


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


def find_shortest_path_bfs(matrix, x_start, y_start, x_end, y_end):
	# assuming start and end are withing bounds
	# let 0 be black (can't visit)
	# let 1 be white (can visit)
	lenrows, lencols = matrix.shape
	# print('rows', lenrows)
	# print('cols', lencols)
	vector_matrix = np.empty((lenrows, lencols), dtype=object)
	for r in range(lenrows):
		for c in range(lencols):
			# print(matrix[0][0])
			vector_matrix[r][c] = Vertex(c, r)
			vector_matrix[r][c].condition = matrix[r][c]
	# vectorMatrix[y_start][x_start].condition = -1
	vector_matrix[y_end][x_end].condition = -2
	queue = list()
	queue.append((x_start, y_start))
	node_count = 1
	while len(queue) > 0:
		visiting_node = queue.pop(0)
		node_count += 1
		# print('visiting', visiting_node[0], visiting_node[1])
		neighbors = get_neighbors(vector_matrix, visiting_node[1], visiting_node[0])
		for neighbor in neighbors:
			neighbor.processed = True
			neighbor.xParent = visiting_node[0]
			neighbor.yParent = visiting_node[1]
			if neighbor.condition == -2:
				# print('found')
				path = []
				iter_v = neighbor
				path.append((x_end, y_end))
				# print('itertype1')
				# print(type(iter_v))
				while iter_v.y != y_start or iter_v.x != x_start:
					path.append((iter_v.x, iter_v.y))
					# print(iter_v.xParent)
					# print(iter_v.yParent)
					iter_v = vector_matrix[iter_v.yParent][iter_v.xParent]
					# print('itertype2')
					# print(type(iter_v))
					# print('test2')
				return path, node_count
			else:
				queue.append((neighbor.x, neighbor.y))
	print('not found')
	return None, node_count
