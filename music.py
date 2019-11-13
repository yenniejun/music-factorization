# This is like prime factorization of a scale, for me

from itertools import cycle
from enum import Enum


# Maps each note in the 12-tone scale to a distinct number
TWELVE_TONE = ['C', 'CSHARP', 'D', 'DSHARP', 'E', 'F', 
'FSHARP', 'G', 'GSHARP', 'A', 'ASHARP', 'B']

TWELVE_TONE = {1:'C', 2:'CSHARP', 3:'D', 4:'DSHARP', 5:'E', 6:'F', 
7:'FSHARP', 8:'G', 9:'GSHARP', 10:'A', 11:'ASHARP', 12:'B'}

TWELVE_TONE = {'C':1, 'CSHARP':2, 'D':3, 'DSHARP':4, 'E':5, 'F':6, 
'FSHARP':7, 'G':8, 'GSHARP':9, 'A':10, 'ASHARP':11, 'B':12}

# Test cale should not repeat any notes on either end of octave
TEST_SCALE = ['C', 'D', 'E', 'G', 'A', 'B', 'C'] 

pentatonic = [1, 3, 5, 8, 10, 12]
pentatonic2 = [3,5,8,10,12,1]

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

def map_num_to_interval(my_number):
	switch()

def convert_scale:
	# TODO: convert scale from letters to numbers
	# TODO: If last note is same as first note mod, then remove last note



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
		scale = (input_scale * 2)[:-1]
	else:
		scale = input_scale # double the scale so we have one full cycle
	
	max_chunk = chunk = 1;
	max_seq_head = seq_head = -1;
	# counting number of diminished intervals in this cycle
	for i in range(0, len(scale)-1):
		# print((scale[i]+interval) % 12, scale[(i+1)%len(scale)] % 12)
		if ((scale[i]+interval) % 12)  == scale[(i+1)%len(scale)] % 12:
			if (seq_head == -1) :
				seq_head = i
			chunk += 1
		else:
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
	while (scale_remainder > 0 and repeat_counter < repeat and index!=-1):
		# print('scale components:', scale_components)
		starting_index = index + len_chunk
		ending_index = index + len_scale
		index, len_chunk = find_longest_chunk((scale*2)[starting_index:ending_index], interval)
		# print('   index:', index, starting_index, ending_index)
		# print('   scale:', (scale*2)[starting_index:ending_index], interval)
		if (index == -1): 
			# print('NEGATIVE')
			return scale_components
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
	pool = cycle(list_of_intervals)
	while (mask != temp):
		results = find_scale_components(next(pool), temp, 2)
		full_results += results
		for result in results:
			temp[result['index'] : result['index']+result['len_chunk']] = [-1] * result['len_chunk']
		results = []
	return full_results


def print_results(results):
	for result in results:
		interval_name = intervals[result['interval']]
		note_count = result['len_chunk']
		starting_index = result['index']
		print(note_count, interval_name, "starting at index", starting_index)



# For Pentatonic
scale = [1, 3, 5, 8, 10, 12]
list_of_intervals1 = [DIM, DIM, DIM, WHT, WHT, CHR, UNI]
print_results(fetch_scale_components(list_of_intervals1, scale))
list_of_intervals2 = [WHT, WHT, CHR, UNI]
print_results(fetch_scale_components(list_of_intervals2, scale))



