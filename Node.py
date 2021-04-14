class Node:
	def __init__(self, x, y, x_parent, y_parent):
		self.x = x
		self.y = y
		self.x_parent = x_parent
		self.y_parent = y_parent
		self.condition = -1


class NodeBFS(Node):
	def __init__(self, x, y, x_parent, y_parent):
		Node.__init__(x, y, x_parent, y_parent)
		self.processed = False
		self.queue_index = -1

	def get_neighbors


class NodeAStar(Node):
	pass
