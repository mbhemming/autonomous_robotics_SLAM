import math
import numpy as np

def MapXYToOccupancyCell(mapXorY):
	return math.floor(mapXorY/12)+1
		
class CourseMap:
		
	def __init__(self):
		self.occupancyGrid = np.zeros((25,29), dtype=np.bool_)
		self.occupancyGrid[0,:]=True
		self.occupancyGrid[:,0]=True
		self.occupancyGrid[24,:]=True
		self.occupancyGrid[:,28]=True
		self.mapGrid = np.zeros((279,326), dtype=np.bool_)
		
	def UpdateOccupancy(self, x, y,isOccupied):
		row = math.floor(y)
		col = math.floor(x)
		self.occupancyGrid[row,col] = isOccupied
		self.mapGrid[(row-1)*12:((row-1)*12)+12,(col-1)*12:((col-1)*12)+12] = isOccupied
		

		
	def UpdateMap(self,x,y,isOccupied):
		row = math.floor(y)
		col = math.floor(x)
		self.mapGrid[row,col] = isOccupied
		self.occupancyGrid[MapXYToOccupancyCell(row),MapXYToOccupancyCell(col)] = isOccupied
	
	def XYOccupied(self, x, y):
		row = math.floor(y)
		col = math.floor(x)
		return self.occupancyGrid[row,col]