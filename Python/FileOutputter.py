import csv
import numpy


def AppendToCsv(csvFile, bot, data):
	writer = csv.writer(csvFile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for row in data:
		#print(row)
		writer.writerow([str(bot.Pose.Pt.x), str(bot.Pose.Pt.y), str(bot.Pose.Theta),\
                                 str(row[0]), str(row[1]), str(row[2])])
