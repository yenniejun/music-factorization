from itertools import chain
from enum import Enum
import unittest

TWELVE_TONES = {'C':1, 'CSHARP':2, 'D':3, 'DSHARP':4, 'EFLAT':4, 'E':5, 'F':6, 
'FSHARP':7, 'G':8, 'GSHARP':9, 'AFLAT':9, 'A':10, 'ASHARP':11, 'BFLAT': 11, 'B':12}

# TODO clean up the globals, it's a bit messy now...
intervals = { 
	0: "UNISON",
	1: "CHROMATIC",
	2: "WHOLE TONE",
	3: "DIMINISHED",
	4: "AUGMENTED",
	6: "TRITONE",
	12: "OCTAVE"
}

UNI = 0
CHR = 1
WHT = 2
DIM = 3
AUG = 4
TRI = 6
OCT = 12

class TestMethods

def convert_scale(raw_scale):
	scale = []
	for letter in raw_scale:
		scale.append(TWELVE_TONES[letter])
	if (scale[-1] == scale[0] and scale[-1] < scale[-2]):
		return scale[:-1]
	return scale
	# TODO: If last note is same as first note mod, then remove last note
	# TODO: Eventually add capability to sort scales 
	# ... OR ... support infinitely high octaves


# Finds the longest contiguous chunk (including wrapping) given params
# 
# PARAMS:
#    - scale: should NOT repeat the octave note 
#    - interval: Should be between 0 and 12. Can be larger but mod 12
#    - wrap (optional): Do you want to wrap the scale to find intervals
#      as part of the cycle? Default set to true..
#      Note: Wraps by doubling then removing last item
#
##### Returns: #####
#  max_seq_head - the index where the longest sequence starts
#  max_chunk - the size of the longest chunk/sequence
def find_longest_chunk(input_scale, interval, wrap=True):
	if wrap: 
		scale = input_scale + [i+12 for i in input_scale[:-1]]
		# scale = (input_scale * 2)[:-1]
	else:
		scale = input_scale # double the scale so we have one full cycle
	max_chunk = chunk = 1;
	max_seq_head = seq_head = 0;
	# counting number of diminished intervals in this cycle
	for i in range(0, len(scale)-1):
		# print('before if', (scale[i%len(scale)]+interval) % 12, scale[(i%len(scale)+1)] % 12)
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



# Finds the components for the given interval, scale, and num of repetitions
# Repetitions means how many times you want to look for instance of
# the given interval in the given scale
def find_scale_components(interval, scale, repeat=1):
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

def fetch_scale_components(list_of_intervals, scale):
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
		# print('full results', full_results)
		for result in results:
			index = result['index']
			chunk = result['len_chunk']
			scale_len = len(scale)
			# print(index, chunk, scale_len)
			if (index+chunk <= scale_len) :
				temp[index:chunk+index] = [-1] * chunk
			else :
				chunk_1 = scale_len - index
				chunk_2 = chunk - chunk_1
				# print('chunks', chunk, chunk_1, chunk_2)
				temp[index:index+chunk_1] = [-1] * chunk_1
				temp[0:chunk_2] = [-1] * chunk_2
		# print(temp)
		results = []
	return full_results


def print_results(results):
	for result in results:
		interval_name = intervals[result['interval']]
		note_count = result['len_chunk']
		starting_index = result['index']
		print(note_count, interval_name, "starting at index", starting_index)



# Testing:
TEST_SCALE = ['C', 'D', 'E', 'G', 'A', 'B', 'C'] 
MAJOR_SCALE = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
MINOR_SCALE = ['C', 'D', 'DSHARP', 'F', 'G', 'GSHARP', 'B', 'C']
DIM_SCALE = ['C', 'DSHARP', '']
scale = convert_scale(MINOR_SCALE)
list_of_intervals1 = [DIM, DIM, DIM, WHT, WHT, CHR]
print_results(fetch_scale_components(list_of_intervals1, scale))
list_of_intervals2 = [WHT, WHT, CHR, UNI]
print_results(fetch_scale_components(list_of_intervals2, scale))

list_of_intervals3 = [AUG, DIM, WHT]
print_results(fetch_scale_components(list_of_intervals3, scale))


