# Queueing Problem
# Author: doodhwala

import random
import sys
import csv

# M = input('Enter the number of checkout counters: ')
M = 2
# N = input('Enter the number of customers: ')
N = 20

MAX_ARRIVAL_TIME = 8
service_time_digits = 2
arrival_time_digits = 3

arrival_times = []
service_times = []

def table_lookup(table, value):
    for row in table:
        l, r = row[3], row[4]
        if(l <= value <= r):
            return row[0]

with open('service_time.in', 'r') as f:
    lines = f.read().split('\n')
    times = int(lines[0])
    cp = 0.0
    rd = 1
    for t in range(1, times + 1):
        time, prob = lines[t].split()
        time, prob = int(time), float(prob)
        cp += prob
        rd_range = int(prob * 10**service_time_digits)
        service_times.append((time, prob, cp, rd, rd + rd_range - 1))
        rd += rd_range

cp = 0.0
rd = 1
for t in range(1, MAX_ARRIVAL_TIME + 1):
    time, prob = t, float(1.0 / MAX_ARRIVAL_TIME)
    cp += prob
    rd_range = int(prob * 10**arrival_time_digits)
    arrival_times.append((time, prob, cp, rd, rd + rd_range - 1))
    rd += rd_range

# Generating data for simulation
customers = []
for i in range(N):
    r_arrival = random.randint(1, 10**arrival_time_digits)
    r_service = random.randint(1, 10**service_time_digits)
    customers.append((r_arrival, r_service))

time = 0
for i in range(N):
    customer = i+1
    time_since_last_arrival = table_lookup(arrival_times, customers[i][0])
    if(i == 0):
        time_since_last_arrival = 0
    arrival_time = time + time_since_last_arrival
    service_time = table_lookup(service_times, customers[i][1])

    customer = {
        "customer": customer,
        "time_since_last_arrival" : time_since_last_arrival,
        "arrival_time" : arrival_time,
        "service_time" : service_time
    }
    customers[i] = customer

counters = [{"free" : True, "time_when_free" : 0} for i in range(M)]
def find_next_free_counter(time):
    next_free = (-1, sys.maxsize)
    for i in range(M):
        if counters[i]["free"]:
            next_free = (i, time)
        else:
            if(next_free[1] > counters[i]["time_when_free"]):
                next_free = (i, counters[i]["time_when_free"])
    return next_free

def update_counters_till(t):
    for counter in counters:
        if(t >= counter["time_when_free"]):
            counter["free"] = True

time = 0
for i in range(N):
    this_customer = customers[i]
    time = this_customer["arrival_time"]
    update_counters_till(time)
    assigned_counter = find_next_free_counter(time)
    this_customer["counter"] = assigned_counter[0]
    this_customer["time_in_queue"] = assigned_counter[1] - time
    this_customer["time_service_begins"] = assigned_counter[1]
    this_customer["time_service_ends"] = this_customer["time_service_begins"] + this_customer["service_time"]
    this_customer["time_in_system"] = this_customer["time_in_queue"] + this_customer["service_time"]

    counter = counters[this_customer["counter"]]
    counter["free"] = False
    counter["time_when_free"] = this_customer["time_service_ends"]


'''
Customer, Time since last arrival, arrival time, service time, time service begins, time customer waits in queue, time service ends, time customer spends in system, ~idle time of server
'''

keys = ['customer', 'time_since_last_arrival', 'arrival_time', 'service_time', 'counter', 'time_service_begins', 'time_in_queue', 'time_service_ends', 'time_in_system']

with open('simulation.csv', 'w', newline='') as csvfile:
    sheet = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    sheet.writerow(keys)
    for customer in customers:
        sheet.writerow([customer[key] for key in keys])
