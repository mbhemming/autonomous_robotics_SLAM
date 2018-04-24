import csv
import numpy
from Robot.Pose import Pose
from OccupancyGrid.OccupancyGrid import OccupancyGrid
import time
def AppendToCsv(csvFile, bot, data):
	writer = csv.writer(csvFile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for row in data:
		#print(row)
		writer.writerow([str(bot.Pose.Pt.x), str(bot.Pose.Pt.y), str(bot.Pose.Theta),\
                                 str(row[0]), str(row[1]), str(row[2])])

def GridToCsv(grid):
	timestr = time.strftime("%Y%m%d-%H%M%S")
	with open(timestr+'_GridOutput.csv', 'w') as csvFile:
		writer = csv.writer(csvFile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for i in range(0, grid.Grid.shape[0]):
		
			row = grid.Grid[grid.Grid.shape[0]-1-i,:]
			writer.writerow(row)
			
