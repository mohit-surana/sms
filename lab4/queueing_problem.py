'''
Queueing Problem
Author: doodhwala

Drive-in Restaurant simulation using future event list
Abdul-Bakra at the counters

'''

import random
import sys
import csv

M = 2
N = 26

MAX_SIMULATION_TIME = 60
service_time_digits = 2
arrival_time_digits = 2

arrival_times = []

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
        rd_range = int(prob * 10**arrival_time_digits)
        arrival_times.append((time, prob, cp, rd, rd + rd_range - 1))
        rd += rd_range

    M = int(lines[times+1])
    lines = lines[times+2:]

    counters = [{} for i in range(M)]
    for i in range(M):
        name, times = lines[0].split()
        times = int(times)
        service_times = []
        cp = 0.0
        rd = 1
        for t in range(1, times + 1):
            time, prob = lines[t].split()
            time, prob = int(time), float(prob)
            cp += prob
            rd_range = int(prob * 10**service_time_digits)
            service_times.append((time, prob, cp, rd, rd + rd_range - 1))
            rd += rd_range
        counters[i]['name'] = name
        counters[i]['service_times'] = service_times
        lines = lines[times+1:]

# Generating data for simulation
arrival_random = [0, 26, 98, 90, 29, 42, 74, 80, 68, 22, 48, 34, 45, 24, 34, 63, 38, 80, 42, 56, 89, 18, 51, 71, 16, 92]
service_random = [95, 21, 51, 92, 89, 38, 13, 61, 50, 49, 39, 53, 88, 1, 81, 53, 81, 64, 1, 67, 1, 47, 75, 57, 87, 47]

La = 1  # State of Abdul (1-available, 0-busy)
Lb = 1  # State of Bakra (1-available, 0-busy)
Wq = 0  # Number of people in waiting queue
Ci = 0  # Cumulative idle time
Cw = 0  # Cumulative wait time

waiting_queue = []

customers_arrived = 0
customers_serviced = 0

# Types of events:
# A - arrival (time, 'A')
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
    FEL.sort()
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

Eg. If it is an arrival, one of these can happen
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
    'La'    : 'La',
    'Lb'    : 'Lb',
    'Wq'    : 'Wq',
    'waiting_queue'  : 'Waiting Queue',
    'FEL'   : 'Future Event List',
    'Ci'    : 'Ci',
    'Cw'    : 'Cw'
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
                        service_time = table_lookup(counters[0]['service_times'], service_random[customers_serviced])
                        addEvent('D', time + service_time, 0)
                    else:
                        Lb = 0
                        service_time = table_lookup(counters[1]['service_times'], service_random[customers_serviced])
                        addEvent('D', time + service_time, 1)
                    customers_serviced += 1
                else:
                    waiting_queue.append(customers_arrived) # Tells about customer number
                    Wq += 1
                customers_arrived += 1
                if(customers_arrived < N):
                    time_to_next_arrival = table_lookup(arrival_times, arrival_random[customers_arrived])
                    addEvent('A', time + time_to_next_arrival)

            elif(event[1] == 'D'):
                if(Wq):
                    if(event[2] == 0):
                        service_time = table_lookup(counters[0]['service_times'], service_random[customers_serviced])
                        addEvent('D', time + service_time, 0)
                    elif(event[2] == 1):
                        service_time = table_lookup(counters[1]['service_times'], service_random[customers_serviced])
                        addEvent('D', time + service_time, 1)
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
