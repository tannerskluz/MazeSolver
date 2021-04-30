class Node:
	def __init__(self, col, row):
		# self.x = x
		self.col = col
		# self.y = y
		self.row = row
		# self.col_parent = col_parent
		# self.row_parent = row_parent
		self.parent_node = None
		self.condition = None


class NodeBFS(Node):
	def __init__(self, col, row):
		Node.__init__(self, col, row)
		self.processed = False
		self.queue_index = None


class NodeAStar(Node):
	def __init__(self, col, row, f_score=float('inf'), g_score=float('inf')):
		Node.__init__(self, col, row)
		self.f_score = f_score
		self.g_score = g_score
		self.closed = False
		self.out_open_set = True

	def __lt__(self, b):
		return self.f_score < b.f_score
