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
travel_random = [6, 0, 3, 1, 8]

L = 1	# Trucks being loaded
Lq = 0	# Trucks in the loading queue
W = 1	# Trucks being weighed
Wq = 0	# Trucks in the weighing queue
Bl = 0  # Cumulative time trucks being loaded
Bs = 0  # Cumulative time trucks being "scaled"

loading_queue = []
weighing_queue = []

trucks_loaded = 0
trucks_weighed = 0
trucks_travelled = 0

# Types of events:
# ALQ	- arrival at loading queue (time, 'ALQ', 'DTx')
# EL	- end of loading (time, 'EL', 'DTx')
# EW	- end of weighing (time, 'EW', 'DTx')

FEL = []

def addEvent(eventType, timeOfEvent, dumpTruck):
	event = (timeOfEvent, eventType, dumpTruck)
	FEL.append(event)
	FEL.sort(key=lambda x: 1 if x[1] == 'EW' else (2 if x[1] == 'EL' else 3))

def getNextEvents():
	if(FEL):
		event = FEL.pop(0)
		events = [event]
		while(FEL and FEL[0][0] == event[0]):
			events.append(FEL.pop(0))
		return events
	else:
		return []

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

'''
done till here
'''

keys = ['time', 'La', 'Lb', 'Wq', 'waiting_queue', 'FEL', 'Ci', 'Cw']

key_pretty = {
	'time'  : 'Time',
	'La'	: 'La',
	'Lb'	: 'Lb',
	'Wq'	: 'Wq',
	'waiting_queue'  : 'Waiting Queue',
	'FEL'   : 'Future Event List',
	'Ci'	: 'Ci',
	'Cw'	: 'Cw'
}


addEvent('E', 60)
addEvent('A', 0)
customers_arrived += 0

with open('simulation.csv', 'w', newline='') as csvfile:
	sheet = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	sheet.writerow([key_pretty[key] for key in keys])

	time = 0
	while(FEL):
		events = getNextEvents()
		new_time = events[0][0]

		Ci += (new_time - time) * (La + Lb)
		Cw += (new_time - time) * Wq
		time = new_time

		for event in events:
			if(event[1] == 'A'):
				if(La or Lb):
					if(La):
						La = 0
						weigh_time = table_lookup(counters[0]['weigh_times'], weigh_random[customers_weighd])
						addEvent('D', time + weigh_time, 0)
					else:
						Lb = 0
						weigh_time = table_lookup(counters[1]['weigh_times'], weigh_random[customers_weighd])
						addEvent('D', time + weigh_time, 1)
					customers_weighd += 1
				else:
					waiting_queue.append(customers_arrived) # Tells about customer number
					Wq += 1
				customers_arrived += 1
				if(customers_arrived < N):
					time_to_next_load = table_lookup(load_times, load_random[customers_arrived])
					addEvent('A', time + time_to_next_load)

			elif(event[1] == 'D'):
				if(Wq):
					if(event[2] == 0):
						weigh_time = table_lookup(counters[0]['weigh_times'], weigh_random[customers_weighd])
						addEvent('D', time + weigh_time, 0)
					elif(event[2] == 1):
						weigh_time = table_lookup(counters[1]['weigh_times'], weigh_random[customers_weighd])
						addEvent('D', time + weigh_time, 1)
					customers_weighd += 1
					waiting_queue.pop(0)
					Wq -= 1
				else:
					if(event[2] == 0):
						La = 1
					elif(event[2] == 1):
						Lb = 1
			else:
				# Stop allowing more customers
				customers_arrived = N+1 # TODO: Use a better condition flag
		sheet.writerow([time, La, Lb, Wq, waiting_queue, FEL, Ci, Cw])
