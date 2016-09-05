'''
Alternate solution
Author: Shiva Deviah (https://github.com/Coldsp33d)

'''

import numpy as np
import csv
# --------------------------------------------------------------------------------------------------------
class Customer:
	id = 0
	def __init__(self, arrival_time, carhop, time_bw_arrivals, time_service_begins, service_time, id=None):
		if id is None:
			self.id = Customer.id
			Customer.id += 1
		else: 
			self.id = id
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
# --------------------------------------------------------------------------------------------------------

#ARRIVAL_RD = [26, 98, 90, 29, 42, 74, 80, 68, 22, 48, 34, 45, 24, 34, 63, 38, 80, 42, 56, 89, 18, 51, 71, 16, 92]	
#SERVICE_RD = [95, 21, 51, 92, 89, 38, 13, 61, 50, 49, 39, 53, 88, 1, 81, 53, 81, 64, 1, 67, 1, 47, 75, 57, 87, 47]

CLOCK = 0
ARRIVAL_RD = np.random.randint(0, 100, 100)
SERVICE_RD = np.random.randint(0, 100, 100)

arrival_time_table = make_table([(1, 0.25), (2, 0.4), (3, 0.2), (4, 0.15)])
abel_table = make_table([(2, 0.3), (3, 0.28), (4, 0.25),  (5, 0.17)])
baker_table = make_table([(3, 0.35), (4, 0.25),  (5, 0.2), (6, 0.2)])

abel_customer = Customer(0, "Abel", 0, 0, table_lookup(abel_table, SERVICE_RD[0]))
baker_customer = None

EVENT_LIST = [	('A', Customer.id, table_lookup(arrival_time_table, ARRIVAL_RD[Customer.id - 1])), 
				('D', abel_customer.id, abel_customer.service_time), ]
CUST_QUEUE = []

CUSTOMER_LIST = [abel_customer]
SIM_LIST = [['Clock', 'Abel\'s Customer No.', 'Tarrival (Abel)', 'Tstart (Abel)', 'Service time (Abel)', 'Baker\'s Customer No.', 'Tarrival (Abel)', 'Tstart (Abel)', 'Service time (Abel)', 'Future Event List']]
SIM_LIST.append([CLOCK, abel_customer.id, abel_customer.arrival_time, abel_customer.time_service_begins, abel_customer.service_time, None, None, None, None, EVENT_LIST])

while CLOCK < 60:
	EVENT_LIST = sorted(EVENT_LIST, key=lambda x: x[-1])
	SIM_LIST.append([CLOCK, abel_customer.id if abel_customer else None, abel_customer.arrival_time if abel_customer else None, abel_customer.time_service_begins if abel_customer else None, abel_customer.service_time if abel_customer else None, baker_customer.id if baker_customer else None, baker_customer.arrival_time if baker_customer else None, baker_customer.time_service_begins if baker_customer else None, baker_customer.service_time if baker_customer else None, str(EVENT_LIST)])

	next_event = EVENT_LIST.pop(0)

	if CLOCK > 60: break
	CLOCK = next_event[-1]



	if next_event[0] is 'A':
		if len(EVENT_LIST) > 0 and EVENT_LIST[0][0] == 'D' and EVENT_LIST[0][-1] == next_event[-1]:
			t =  EVENT_LIST[0]
			EVENT_LIST[0] = next_event
			next_event = t

		else:	 
			try:
				if len(CUST_QUEUE) == 0:
					EVENT_LIST.append(('A', next_event[1] + 1, table_lookup(arrival_time_table, ARRIVAL_RD[next_event[1]]) + CLOCK))
				else:
					t = max(CUST_QUEUE[-1][0], next_event[1])
					EVENT_LIST.append(('A', t + 1, table_lookup(arrival_time_table, ARRIVAL_RD[t]) + CLOCK))
			except:
				pass

			time_bw_arrivals = table_lookup(arrival_time_table, ARRIVAL_RD[next_event[1] - 1])
			
			if abel_customer is None:
				service_time = table_lookup(abel_table, SERVICE_RD[next_event[1]])
				abel_customer = Customer(CLOCK, "Abel", time_bw_arrivals, CLOCK, service_time)
				EVENT_LIST.append(('D', abel_customer.id, CLOCK + service_time))
				CUSTOMER_LIST.append(abel_customer)

			elif abel_customer is not None and baker_customer is None:
				service_time = table_lookup(baker_table, SERVICE_RD[next_event[1]])
				baker_customer = Customer(CLOCK, "Baker", time_bw_arrivals, CLOCK, service_time)
				EVENT_LIST.append(('D', baker_customer.id, CLOCK + service_time))
				CUSTOMER_LIST.append(baker_customer)

			elif abel_customer is not None and baker_customer is not None:
				if len(CUST_QUEUE) == 0: 
					CUST_QUEUE.append((next_event[1], CLOCK))
				else: 
					CUST_QUEUE.append((CUST_QUEUE[-1][0] + 1, CLOCK))
		
	if next_event[0] is 'D': 
		if abel_customer is not None and next_event[1] == abel_customer.id: 
			abel_customer = None
			if len(CUST_QUEUE) > 0:
				waiting_customer = CUST_QUEUE.pop(0)
				service_time = table_lookup(abel_table, SERVICE_RD[waiting_customer[0]])
				time_bw_arrivals = table_lookup(arrival_time_table, ARRIVAL_RD[waiting_customer[0] - 1])
				abel_customer = Customer(waiting_customer[1], "Abel", time_bw_arrivals, CLOCK, service_time)
				EVENT_LIST.append(('D', abel_customer.id, CLOCK + service_time))
				CUSTOMER_LIST.append(abel_customer)
		
		elif next_event[1] == baker_customer.id:
			baker_customer = None
			if len(CUST_QUEUE) > 0:
				n_next_event = EVENT_LIST[0]
				# if the next customer leaves at the same time, let's wait for Abel
				if n_next_event[0] is 'D' and n_next_event[2] == next_event[2]: 
					pass
				else:
					waiting_customer = CUST_QUEUE.pop(0)
					service_time = table_lookup(baker_table, SERVICE_RD[waiting_customer[0]])
					time_bw_arrivals = table_lookup(arrival_time_table, ARRIVAL_RD[waiting_customer[0] - 1])
					baker_customer = Customer(waiting_customer[1], "Baker", time_bw_arrivals, CLOCK, service_time)
					EVENT_LIST.append(('D', baker_customer.id, CLOCK + service_time))
					CUSTOMER_LIST.append(baker_customer)


# for customer in CUSTOMER_LIST:
# 	print(str(customer))

with open('sim4.csv', 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(SIM_LIST)



