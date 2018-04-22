#!/usr/bin/env python3

import numpy as np


def DecomposeSensorReadings( allReadings, granularity ):

	sortedReadings = np.sort( allReadings )
	#print(sortedReadings)
	
	bins =[]
	
	category = 0
	start = 0
	i = 0
	while i < sortedReadings.size:
		category = sortedReadings[i]
		#print("Category: " + str(category))
		while i<sortedReadings.size and sortedReadings[i]-category < granularity:
			i = i + 1
		if start != i:
			#print(sortedReadings[start:i])
			bins.append(sortedReadings[start:i])
			start = i
		i = i + 1

	#print(bins)
	return bins
