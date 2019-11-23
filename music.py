from itertools import chain

TWELVE_TONES = {'C':1, 'CSHARP':2, 'DFLAT': 2, 'D':3, 'DSHARP':4, 'EFLAT':4, 'E':5, 'F':6, 
'FSHARP':7, 'G':8, 'GSHARP':9, 'AFLAT':9, 'A':10, 'ASHARP':11, 'BFLAT': 11, 'B':12}

INTERVALS = { 0: "UNISON",1: "CHROMATIC",2: "WHOLE TONE",3: "DIMINISHED",
4: "AUGMENTED",6: "TRITONE",12: "OCTAVE"}

UNI = 0; CHR = 1; WHT = 2; DIM = 3; AUG = 4; TRI = 6; OCT = 12

TWELVE = 12

MINUS_MASK = -10000


def convert_scale(raw_scale):
	"""Converts the provided scale to corresponding numbers

	Parameters:
		raw_scale: a scale in letter format, assumed to be 1 octave only

	ToDo: Add capability to sort scales
	ToDo: Add capability to support infinitely high octaves
	"""

	scale = []
	upper_raw_scale = [a.upper() for a in raw_scale]
	for letter in upper_raw_scale:
		if (letter in TWELVE_TONES.keys()):
			scale.append(TWELVE_TONES[letter])
	if (len(scale) > 1 and scale[-1] == scale[0] and scale[-1] < scale[-2]):
		return scale[:-1]
	return scale

def update_max_count(count, max_count, head, max_head):
	""" Returns the updated max count and max head while determining longest count for interval"""
	if count > max_count:
		return (count, head)
	return (max_count, max_head)

def is_correct_interval(i, scale, interval):
	""" Checks if the value at scale[i] is an interval-size from i+1"""
	if i >= len(scale): return False
	return ((scale[i] + interval) % TWELVE) == (scale[i+1] % TWELVE)


def find_longest_count_for_interval(scale, interval):
	"""Finds the longest contiguous chunk of given internval for given scale

	Parameters:
		scale: the scale to search for the longest chunk
		interval: the interval to determine the longest chunk; between 0 and 12

	Returns:
		max_head: index of where the longest sequence starts
		max_count: size of the longest chunk/sequence
	"""
	max_count = count = 1
	max_head = head = -1
	for i in range(0, len(scale) - 1):
		if (is_correct_interval(i, scale, interval)):
			head = i if count == 1 else head
			count += 1
		else:
			max_count, max_head = update_max_count(count, max_count, head, max_head)
			count = 1; head = -1 # reset
	# If max count is same as scale len, then no need to check for wrapping
	if (max_count == len(scale)):
		return (max_head, max_count)
	# Check for wrapping: either continue current streak or start with last element of scale
	head = head if head != -1 else len(scale) - 1
	for i in range(-1, head-1):
		if (is_correct_interval(i, scale, interval)):
			count += 1
		else: #
			break
	max_count, max_head = update_max_count(count, max_count, head, max_head)
	return (max_head, max_count)


def find_scale_components(scale, interval, repeat=1):
	""" Finds the list of scale components for given interval

	Parameters:
		interval: the interval to determine the longest chunk; between 0 and 12
		scale: the scale to search for the longest chunk
		repeat (optional): default set to 1. Determines number of times you want to look for instance of 
			the given interval in the scale

	Returns:
		scale_components: a list with all of the different contiguous components of 
		given interval
	"""

	scale_remainder = len(scale)
	scale_components = []
	index = 0; len_chunk = 0; len_scale = len(scale); repeat_counter = 0;
	while (scale_remainder > 0 and repeat_counter < repeat):
		starting_index = index + len_chunk
		ending_index = index + len_scale
		index, len_chunk = find_longest_count_for_interval(scale[starting_index:ending_index], interval)
		if (index != -1):
			scale_components.append({
				'interval': interval,
				'len_chunk': len_chunk,
				'index': (starting_index + index)%len_scale })
		scale_remainder -= len_chunk
		repeat_counter += 1
	return scale_components


def isDescending(lst):
	"""Returns false if list is not descending"""
	for i in range( len(lst) - 1 ):
		if lst[i] < lst[i+1]:
			return False
		return True
	return True


def fetch_scale_components(list_of_intervals, scale):
	""" Fetches scale components for given list of intervals

	Parameters:
		list_of_intervals: the different intervals you wish to search for in the scale
			MUST be in descending order
		scale: the scale to search for the longest chunk

	Returns:
		full_results: a list with all of the different contiguous components for all the intervlas 
	"""

	if (not isDescending(list_of_intervals)): 
		return []
	mask = [MINUS_MASK] * len(scale)
	temp = scale[:]
	full_results = results = []
	pool = chain(list_of_intervals)
	scale_len = len(scale)
	for interval in list_of_intervals:
		if(mask == temp):
			return full_results
		next_value = next(pool)
		results = find_scale_components(temp, next_value)
		if (len(results)==0):
			continue
		full_results += results
		for result in results:
			index = result['index']
			chunk = result['len_chunk']
			if (index+chunk <= scale_len) :
				temp[index:chunk+index] = [MINUS_MASK] * chunk
			else :
				chunk_1 = scale_len - index
				chunk_2 = chunk - chunk_1
				temp[index:index+chunk_1] = [MINUS_MASK] * chunk_1
				temp[0:chunk_2] = [MINUS_MASK] * chunk_2
		results = []
	return full_results


def print_results(results):
	"""Prints the results in a nicer format"""
	for result in results:
		interval_name = INTERVALS[result['interval']]
		note_count = result['len_chunk']
		starting_index = result['index']
		print(note_count, interval_name, "starting at index", starting_index)
