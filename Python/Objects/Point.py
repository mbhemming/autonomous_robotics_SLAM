	
class Point:
		
	def __init__( self, x = 0, y = 0 ):
		self.x = 0
		self.y = 0
	
	def __str__(self):
        return "( %s, %s )" % ( self.x, self.y)
