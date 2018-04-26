import csv
import numpy
#from Pose import Pose
from OccupancyGrid import OccupancyGrid
import time

def AppendToCsv(csvFile, bot, data):
	writer = csv.writer(csvFile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for row in data:
		#print(row)
		writer.writerow([str(bot.x), str(bot.y), str(bot.Theta),\
                                 str(row[0]), str(row[1]), str(row[2])])

def GridToCsv(grid, appendy="_noname_"):
	timestr = time.strftime("%H%M%S")
	with open(timestr+appendy+'_GridOutput.csv', 'w') as csvFile:
		writer = csv.writer(csvFile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for i in range(0, grid.Grid.shape[0]):
		
			row = grid.Grid[grid.Grid.shape[0]-1-i,:]
			writer.writerow(row)
			
def CsvToGrid(filename, cellsz):
	g = OccupancyGrid( cellsz )
	with open(filename, 'rb') as csvFile:
		reader = csv.reader(csvFile)
		rows = []
		i = 0
		for row in reader:
			g.Grid[i] = row
			i = i + 1
	return g
		
		
