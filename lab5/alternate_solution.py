import csv


LOADING_RD = [71, 16, 24, 63, 98, 42, 55]
WEIGHING_RD = [23, 47, 8, 93, 51, 84]
TRAVEL_RD = [6, 0, 3, 1, 8]
MAX_TIME_LIMIT = 60

class Dumper:
	def __init__(self, id):
		self.id = id

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

def print_items_in_queue(list):
	t = []
	for item in list: 
		t.append("DT" + str(item.id))

	return t

loading_table = make_table([ (5, 0.3), (10, 0.5), (15, 0.2) ])
travel_table = make_table([ (40, 0.4), (60, 0.3), (80, 0.2), (100, 0.1) ])
weighing_table = make_table([(12, 0.7), (16, 0.3)])

loader_1 = Dumper(id=2)
loader_2 = Dumper(id=3)
scale = Dumper(id=1)

LOAD_QUEUE = [Dumper(id=4), Dumper(id=5), Dumper(id=6)]
SCALE_QUEUE = []
EVENT_LIST = [	('EW', 1, table_lookup(weighing_table, WEIGHING_RD[0])), 
				('EL', 2, table_lookup(loading_table, LOADING_RD[0])), 
				('EL', 3, table_lookup(loading_table, LOADING_RD[1])) ]
				
SIM_LIST = [['Clock', 'LQ(t)', 'L(t)', 'WQ(t)', 'W(t)', 'Loading Queue', 'Weighing Queue', 'Future Event List']]
weighing_ctr = 1
loading_ctr = 2
travel_ctr = 0

CLOCK = 0

while (len(EVENT_LIST) > 0):
	EVENT_LIST = sorted(EVENT_LIST, key=lambda x: x[-1])
	
	t = 0
	if loader_1 is not None:
		if loader_2 is not None: 
			t = 2
		else: 
			t = 1
			
				
	SIM_LIST.append([CLOCK, len(LOAD_QUEUE), t, len(SCALE_QUEUE), 1 if scale else 0, print_items_in_queue(LOAD_QUEUE), print_items_in_queue(SCALE_QUEUE), EVENT_LIST])
	 
	next_event = EVENT_LIST.pop(0)
	CLOCK = next_event[-1]
	
	if next_event[0] == 'EL':
		if loader_1.id == next_event[1]:
			temp = loader_1
			if len(LOAD_QUEUE) > 0: # if loading queue is not empty, assign him to the queue
				loader_1 = LOAD_QUEUE.pop(0)
				try:
					EVENT_LIST.append(('EL', loader_1.id, CLOCK + table_lookup(loading_table, LOADING_RD[loading_ctr])))
				except: 
					pass
				loading_ctr += 1
			
		elif loader_2.id == next_event[1]:
			temp = loader_2
			if len(LOAD_QUEUE) > 0:
				loader_2 = LOAD_QUEUE.pop(0)
				try:
					EVENT_LIST.append(('EL', loader_2.id, CLOCK + table_lookup(loading_table, LOADING_RD[loading_ctr])))
				except:
					pass
				loading_ctr += 1
			
		if scale is None:
			scale = temp
			try:
				EVENT_LIST.append(('EW', scale.id, CLOCK + table_lookup(weighing_table, WEIGHING_RD[weighing_ctr])))
			except: 
				pass
			weighing_ctr += 1
		else:
			SCALE_QUEUE.append(temp)
			
	elif next_event[0] == 'EW':
		try:
			EVENT_LIST.append(('ALQ', scale.id, CLOCK + table_lookup(travel_table, TRAVEL_RD[travel_ctr])))
		except: 
			pass
		travel_ctr += 1
		if len(SCALE_QUEUE) > 0:
			scale = SCALE_QUEUE.pop(0)
			try:
				EVENT_LIST.append(('EW', scale.id, CLOCK + table_lookup(weighing_table, WEIGHING_RD[weighing_ctr])))
			except: 
				pass
			weighing_ctr += 1
			
	
	elif next_event[0] == 'ALQ':
		if loader_1 is None:
			loader_1 = Dumper(id=next_event[1])
			try:
				EVENT_LIST.append(('EL', loader_1.id, CLOCK + table_lookup(loading_table, LOADING_RD[loading_ctr])))
			except: 
				pass
			loading_ctr += 1
		elif loader_2 is None:
			loader_2 = Dumper(id=next_event[1])
			try:
				EVENT_LIST.append(('EL', loader_2.id, CLOCK + table_lookup(loading_table, LOADING_RD[loading_ctr])))
			except: 
				pass
			loading_ctr += 1
		
		elif loader_1 is not None and loader_2 is not None:
			LOAD_QUEUE.append(Dumper(id=next_event[1]))
		
with open('sim5.csv', 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerows(SIM_LIST)
					
	

