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

'''
done till here
'''
# Generating data for simulation
loading_random = [71, 16, 24, 63, 98, 42, 55]
weighing_random = [23, 47, 8, 93, 51, 84]
travel_random = [6, 0, 3, 1, 8]

La = 1  # State of Abdul (1-available, 0-busy)
Lb = 1  # State of Bakra (1-available, 0-busy)
Wq = 0  # Number of people in waiting queue
Ci = 0  # Cumulative idle time
Cw = 0  # Cumulative wait time

waiting_queue = []

customers_arrived = 0
customers_weighd = 0

# Types of events:
# A - load (time, 'A')
# D - departure (time, 'D', counter)
# E - end of simulation (time, 'E')

FEL = []

def addEvent(eventType, timeOfEvent, counter=-1):
	event = 0
	if(eventType != 'D'):
		event = (timeOfEvent, eventType)
	else:
		event = (timeOfEvent, eventType, counter)
	FEL.append(event)
	FEL.sort(key=lambda x: x[0] - (0.5 if x[1] == 'D' else 0)  - (0.2 if (x[1] == 'D' and x[2] == 0) else 0) )
	# TODO: Convert into insertion instead of sort

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

Main thing is, we look at the top most event and handle it by event type

Eg. If it is an load, one of these can happen
Abel is free and now he becomes busy
	change abel's status and add a departure event for the customer
Abel is busy but Baker is free
	change Baker's status and add a departure event for the customer
Both are busy
	Add to the queue

If it is a departure,
See which counter he was in and change the status for that.
If there are people in the waiting queue, put them into the counter (and add their departure event)

If it is end of simulation, stop accepting more customers
But finish the current customers in the counters / queue
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
