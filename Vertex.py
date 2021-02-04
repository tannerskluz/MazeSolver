class Vertex:
	def __init__(self, x_coordinate, y_coordinate):
		self.x = x_coordinate
		self.y = y_coordinate
		self.xParent = None
		self.yParent = None
		self.processed = False
		self.queueIndex = None