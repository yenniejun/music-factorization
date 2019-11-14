from itertools import chain

TWELVE_TONES = {'C':1, 'CSHARP':2, 'DFLAT': 2, 'D':3, 'DSHARP':4, 'EFLAT':4, 'E':5, 'F':6, 
'FSHARP':7, 'G':8, 'GSHARP':9, 'AFLAT':9, 'A':10, 'ASHARP':11, 'BFLAT': 11, 'B':12}

intervals = { 0: "UNISON",1: "CHROMATIC",2: "WHOLE TONE",3: "DIMINISHED",
4: "AUGMENTED",6: "TRITONE",12: "OCTAVE"}

UNI = 0; CHR = 1; WHT = 2; DIM = 3; AUG = 4; TRI = 6; OCT = 12


def convert_scale(raw_scale):
	"""Converts the provided scale to corresponding numbers

	Parameters:
		raw_scale: a scale in letter format, assumed to be 1 octave only

	ToDo: Add capability to sort scales
	ToDo: Add capability to support infinitely high octaves
	"""

	scale = []
	for letter in raw_scale:
		if (letter in TWELVE_TONES.keys()):
			scale.append(TWELVE_TONES[letter])
	if (len(scale) > 1 and scale[-1] == scale[0] and scale[-1] < scale[-2]):
		return scale[:-1]
	return scale


def find_longest_chunk(input_scale, interval, wrap=True):
	"""Finds the longest contiguous chunk of given internval for given scale

	Parameters:
		input_scale: the scale to search for the longest chunk
		interval: the interval to determine the longest chunk; between 0 and 12
		wrap (optional): default true; determines if you wish to wrap to scale 
			Wrapping is done by doubling the original scale, adding 12, then removing last item

	Returns:
		max_seq_head: index of where the longest sequence starts
		max_chunk: size of the longest chunk/sequence
	"""

	if wrap: 
		scale = input_scale + [i+12 for i in input_scale[:-1]]
	else:
		scale = input_scale # double the scale so we have one full cycle
	max_chunk = chunk = 1;
	max_seq_head = seq_head = 0;
	# counting number of diminished intervals in this cycle
	for i in range(0, len(scale)-1):
		current_index = i 
		next_index = i + 1
		current_value = scale[i]
		next_value = scale[i+1]
		if (current_value + interval == next_value):
			if (chunk == 1) :
				seq_head = i
			chunk += 1
		else :
			if (chunk > max_chunk):
				max_chunk = chunk
				max_seq_head = seq_head
			chunk = 1 # reset
			seq_head = -1 #reset
	if (chunk > max_chunk):
		max_chunk = chunk
		max_seq_head = seq_head
	return (max_seq_head, max_chunk)


def find_scale_components(interval, scale, repeat=1):
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
	index = 0
	len_chunk = 0
	len_scale = len(scale)
	repeat_counter = 0;
	while (scale_remainder > 0 and repeat_counter < repeat):
		starting_index = index + len_chunk
		ending_index = index + len_scale
		index, len_chunk = find_longest_chunk(scale[starting_index:ending_index], interval)
		if (len_chunk >1):
			scale_components.append({'interval': interval,
							'len_chunk': len_chunk,
							'index': (starting_index + index)%len_scale
							 })
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
	if (isDescending(list_of_intervals) == False): 
		return []
	mask = [-1] * len(scale)
	temp = scale[:]
	full_results = results = []
	pool = chain(list_of_intervals)
	for interval in list_of_intervals:
		if(mask == temp):
			return full_results
		next_value = next(pool)
		results = find_scale_components(next_value, temp)
		if (len(results)==0):
			continue
		full_results += results
		for result in results:
			index = result['index']
			chunk = result['len_chunk']
			scale_len = len(scale)
			if (index+chunk <= scale_len) :
				temp[index:chunk+index] = [-1] * chunk
			else :
				chunk_1 = scale_len - index
				chunk_2 = chunk - chunk_1
				temp[index:index+chunk_1] = [-1] * chunk_1
				temp[0:chunk_2] = [-1] * chunk_2
		results = []
	return full_results


def print_results(results):
	"""Prints the results in a nicer format"""
	for result in results:
		interval_name = musicenums.intervals[result['interval']]
		note_count = result['len_chunk']
		starting_index = result['index']
		print(note_count, interval_name, "starting at index", starting_index)
