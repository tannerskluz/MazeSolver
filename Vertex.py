class Vertex:
	def __init__(self, x_coordinate, y_coordinate, fscore = float('inf'), gscore = float('inf')):
		self.x = x_coordinate
		self.y = y_coordinate
		self.xParent = None
		self.yParent = None
		self.processed = False
		self.queueIndex = None
		self.condition = None
		#additions for aStar
		self.fscore = fscore
		self.gscore = gscore
		self.closed = False
		self.out_openset = True