'''
Alternate solution
Author: Shiva Deviah (https://github.com/Coldsp33d)

'''

import numpy as np
import time

MAX_SIM_TIME = 60
ARRIVAL_RD = np.random.randint(0, 100, 100)
SERVICE_RD = np.random.randint(0, 100, 100)

class Customer:
	id = 0
	def __init__(self, arrival_time, carhop, time_bw_arrivals, time_service_begins, service_time):
		self.id = Customer.id
		Customer.id += 1
		self.arrival_time = arrival_time
		self.carhop = carhop
		self.time_bw_arrivals = time_bw_arrivals 
		self.time_service_begins = time_service_begins
		self.service_time = service_time
		
	def __str__(self):
		time_service_ends = self.time_service_begins + self.service_time
		time_in_queue = self.time_service_begins - self.arrival_time
		return str(self.id + 1) + "\t" + str(self.time_bw_arrivals) + "\t" + str(self.arrival_time) + "\t" + str(self.carhop) + "\t" +  str(self.time_service_begins) + "\t" + str(self.service_time) + "\t" + str(time_service_ends) + "\t" + str(time_in_queue)
		
def make_table(values):
	table = []
	
	for i, entry in enumerate(values):
		if i == 0: 
			s = 0
			e = int(entry[1] * 100)
		else: 
			s = int(table[-1][2] + 1)
			e = int(s + entry[1] * 100 - 1)
		table.append((entry[0], s, e))
		
	return table

def table_lookup(table, number):
	for entry in table:
		if entry[1] <= number <= entry[2]:
			return entry[0]
	
arrival_time_table = make_table([(1, 0.25), (2, 0.4), (3, 0.2), (4, 0.15)])
abel_table = make_table([(2, 0.3), (3, 0.28), (4, 0.25),  (5, 0.17)])
baker_table = make_table([(3, 0.35), (4, 0.25),  (5, 0.2), (6, 0.2)])

CUSTOMER_LIST = []
CLOCK = 0 # simulate for 60 minutes

abel_free_at = CLOCK
baker_free_at = CLOCK

arrival_time = 0
service_time = table_lookup(abel_table, SERVICE_RD[0])
abel_free_at = CLOCK + service_time
CUSTOMER_LIST.append(Customer(0, "Abel", 0, 0, service_time))

while CLOCK < MAX_SIM_TIME:
	try:
		time_bw_arrivals = table_lookup(arrival_time_table, ARRIVAL_RD[Customer.id - 1])
	except: 
		break
	CLOCK = arrival_time = CLOCK + time_bw_arrivals
	if(CLOCK > 60): break
	
	if abel_free_at <= CLOCK or abel_free_at <= baker_free_at:
		time_service_begins = max(CLOCK, abel_free_at)
		carhop = "Abel"
		service_time = table_lookup(abel_table, SERVICE_RD[Customer.id])
		abel_free_at = time_service_begins + service_time
	
	elif baker_free_at <= CLOCK or baker_free_at < abel_free_at:
		time_service_begins = max(CLOCK, baker_free_at)
		carhop = "Baker"
		service_time = table_lookup(baker_table, SERVICE_RD[Customer.id])
		baker_free_at = time_service_begins + service_time
	
	CUSTOMER_LIST.append(Customer(arrival_time, carhop, time_bw_arrivals, time_service_begins, service_time))

for customer in CUSTOMER_LIST:
	print str(customer)
	time.sleep(0.2)

 
"""
ARRIVAL_RD = [26, 98, 90, 29, 42, 74, 80, 68, 22, 48, 34, 45, 24, 34, 63, 38, 80, 42, 56, 89, 18, 51, 71, 16, 92]	
SERVICE_RD = [95, 21, 51, 92, 89, 38, 13, 61, 50, 49, 39, 53, 88, 1, 81, 53, 81, 64, 1, 67, 1, 47, 75, 57, 87, 47]
"""
