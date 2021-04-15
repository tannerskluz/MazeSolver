class Node:
	def __init__(self, col, row):
		# self.x = x
		self.col = col
		# self.y = y
		self.row = row
		# self.col_parent = col_parent
		# self.row_parent = row_parent
		self.parent_node = None
		self.condition = -1


class NodeBFS(Node):
	def __init__(self, col, row):
		Node.__init__(self, col, row)
		self.processed = False
		self.queue_index = -1


class NodeAStar(Node):
	def __init__(self, col, row):
		Node.__init__(self, col, row)
		self.f_score = 0
		self.g_score = 0
		self.closed = False
		self.out_open_set = True

	def __lt__(self, b):
		return self.f_score < b.f_score
