'''
Dump Truck Problem
Author: doodhwala

Dump Truck Problem using Future Event List

'''

import random
import sys
import csv

M = 2
N = 26

MAX_SIMULATION_TIME = 60
load_time_digits = 2
weigh_time_digits = 2
travel_time_digits = 1

load_times = []
weigh_times = []
travel_times = []

def table_lookup(table, value):
	for row in table:
		l, r = row[3], row[4]
		if(l <= value <= r):
			return row[0]

with open('input.in', 'r') as f:
	lines = f.read().split('\n')
	times = int(lines[0])
	cp = 0.0
	rd = 1
	for t in range(1, times + 1):
		time, prob = lines[t].split()
		time, prob = int(time), float(prob)
		cp += prob
		rd_range = int(prob * 10**load_time_digits)
		load_times.append((time, prob, cp, rd, rd + rd_range - 1))
		rd += rd_range
	lines = lines[times+1:]

	times = int(lines[0])
	cp = 0.0
	rd = 1
	for t in range(1, times + 1):
		time, prob = lines[t].split()
		time, prob = int(time), float(prob)
		cp += prob
		rd_range = int(prob * 10**weigh_time_digits)
		weigh_times.append((time, prob, cp, rd, rd + rd_range - 1))
		rd += rd_range
	lines = lines[times+1:]

	times = int(lines[0])
	cp = 0.0
	rd = 1
	for t in range(1, times + 1):
		time, prob = lines[t].split()
		time, prob = int(time), float(prob)
		cp += prob
		rd_range = int(prob * 10**travel_time_digits)
		travel_times.append((time, prob, cp, rd, rd + rd_range - 1))
		rd += rd_range

# Generating data for simulation
loading_random = [71, 16, 24, 63, 98, 42, 55]
weighing_random = [23, 47, 8, 93, 51, 84]
travel_random = [6, 10, 3, 1, 8]

# Types of events:
# ALQ	- arrival at loading queue (time, 'ALQ', DTx)
# EL	- end of loading (time, 'EL', DTx)
# EW	- end of weighing (time, 'EW', DTx)

FEL = []

def addEvent(eventType, timeOfEvent, dumpTruck):
	event = (timeOfEvent, eventType, dumpTruck)
	FEL.append(event)
	FEL.sort(key=lambda x: x[0] + (0.1 if x[1] == 'EW' else (0.2 if x[1] == 'EL' else 0.3)))

def getNextEvents():
	if(FEL):
		event = FEL.pop(0)
		events = [event]
		while(FEL and FEL[0][0] == event[0]):
			events.append(FEL.pop(0))
		return events
	else:
		return []

keys = ['time', 'L', 'Lq', 'W', 'Wq', 'loading_queue', 'weighing_queue', 'FEL', 'Bl', 'Bs']

key_pretty = {
	'time'  : 'Time',
	'L'		: 'L',
	'Lq'	: 'Lq',
	'W'		: 'W',
	'Wq'	: 'Wq',
	'loading_queue'  : 'Loading Queue',
	'weighing_queue'  : 'Weighing Queue',
	'FEL'   : 'Future Event List',
	'Bl'	: 'Bl',
	'Bs'	: 'Bs'
}

'''
Logic:

Look at the top most event and handle it by event type:

EW
	A dump truck has finished getting weighed.
	Now it will start a travel time back to the loaders
	Add an ALQ event
	If someone is in the weighing queue, add EW event for it
	Else, change status

EL
	A dump truck has finished getting loaded.
	Now it will go to get weighed
		If there is a free weighing scale, then add an EW event
		If not, add the truck to the weighing queue
	If there is someone in the loading queue, add EL event for it
	Else, change status

ALQ
	A dump truck has arrived to get loaded
	If there is a free loader, then add EL event for it
	Else, add the truck to the loading queue

'''

L	= 2	# Trucks being loaded
Lq	= 3	# Trucks in the loading queue
W	= 1	# Trucks being weighed
Wq	= 0	# Trucks in the weighing queue
Bl	= 0	# Cumulative time trucks being loaded
Bs	= 0	# Cumulative time trucks being "scaled"

loading_queue = [4, 5, 6]
weighing_queue = []

trucks_loaded = 0
trucks_weighed = 0
trucks_travelled = 0

time = 0

# TODO: Find a cleaner way of handing the initial state

weigh_time = table_lookup(weigh_times, weighing_random[trucks_weighed])
addEvent('EW', time + weigh_time, 1)
trucks_weighed += 1

load_time = table_lookup(load_times, loading_random[trucks_loaded])
addEvent('EL', time + load_time, 2)
trucks_loaded += 1

load_time = table_lookup(load_times, loading_random[trucks_loaded])
addEvent('EL', time + load_time, 3)
trucks_loaded += 1

with open('simulation.tsv', 'w', newline='') as csvfile:
	sheet = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	sheet.writerow([key_pretty[key] for key in keys])
	sheet.writerow([time, L, Lq, W, Wq, loading_queue, weighing_queue, FEL, Bl, Bs])
	while(FEL):
		events = getNextEvents()
		new_time = events[0][0]

		Bl += (new_time - time) * L
		Bs += (new_time - time) * W
		time = new_time

		if(trucks_loaded == len(loading_random)):
			events = [event for event in events if event[1] != 'ALQ']
		if(trucks_weighed == len(weighing_random)):
			events = [event for event in events if event[1] != 'EL']
		if(trucks_travelled == len(travel_random)):
			events = [event for event in events if event[1] != 'EW']

		for event in events:
			if(event[1] == 'ALQ'):
				if(L < 2):
					L += 1
					load_time = table_lookup(load_times, loading_random[trucks_loaded])
					addEvent('EL', time + load_time, event[2])
					trucks_loaded += 1
				else:
					loading_queue.append(event[2])
					Lq += 1

			elif(event[1] == 'EL'):
				if(W < 1):
					W += 1
					weigh_time = table_lookup(weigh_times, weighing_random[trucks_weighed])
					addEvent('EW', time + weigh_time, event[2])
					trucks_weighed += 1
				else:
					weighing_queue.append(event[2])
					Wq += 1

				if(Lq):
					Lq -= 1
					load_time = table_lookup(load_times, loading_random[trucks_loaded])
					addEvent('EL', time + load_time, loading_queue.pop(0))
					trucks_loaded += 1
				else:
					L -= 1

			elif(event[1] == 'EW'):
				travel_time = table_lookup(travel_times, travel_random[trucks_travelled])
				addEvent('ALQ', time + travel_time, event[2])
				trucks_travelled += 1

				if(Wq):
					Wq -= 1
					weigh_time = table_lookup(weigh_times, weighing_random[trucks_weighed])
					addEvent('EW', time + weigh_time, weighing_queue.pop(0))
					trucks_weighed += 1
				else:
					W -= 1
		sheet.writerow([time, L, Lq, W, Wq, loading_queue, weighing_queue, FEL, Bl, Bs])
