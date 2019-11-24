import unittest
import music

class Tests(unittest.TestCase):

	##### convert_scale ######

	def test_convert_scale_normal(self):
		assert music.convert_scale(['C','D','E','G','A','B','C']) == [1,3,5,8,10,12]
		
	def test_convert_scale_accidentals(self):
		assert music.convert_scale(['CSHARP', 'DFLAT', 'D', 'DSHARP']) == [2,2,3,4]
		
	def test_convert_scale_incorrect(self):
		assert music.convert_scale(['BLAH']) == []

	def test_convert_scale_blank(self):
		assert music.convert_scale([]) == []

	###### is_correct_interval #####

	def test_is_correct_interval_true(self):
		assert(music.is_correct_interval(1, [1,2,3], 1) == True)

	def test_is_correct_interval_false(self):
		assert(music.is_correct_interval(1, [1,2,3], 2) == False)

	def test_is_correct_interval_false_oob(self):
		assert(music.is_correct_interval(3, [1,2,3], 1) == False)

	def test_is_correct_interval_matches_mask(self):
		assert(music.is_correct_interval(0, [music.MINUS_MASK, 10], 2) == False)

	##### update_max_count #####

	def test_update_max_count_old_max(self):
		_max_count, _max_head = music.update_max_count(1,10,2,20)
		assert(_max_count == 10 and _max_head == 20)

	def test_update_max_count_new_max(self):
		_max_count, _max_head = music.update_max_count(10,1,20,2)
		assert(_max_count == 10 and _max_head == 20)

	##### find_longest_count_for_interval #####

	def test_find_longest_count_normal_case(self):
		_index, _count = music.find_longest_count_for_interval([1,2,3,4,5],1)
		assert(_index == 0 and _count == 5)

	def test_find_longest_count_longest_chunk_at_beginning(self):
		_index, _count = music.find_longest_count_for_interval([1,3,5,7,8,10],2)
		assert(_index == 0 and _count == 4)	

	def test_find_longest_count_longest_chunk_at_end(self):
		_index, _count = music.find_longest_count_for_interval([3,5,6,8,10,12],2)
		assert(_index == 2 and _count == 4)		

	def test_find_longest_count_extra_noise(self):
		_index, _count = music.find_longest_count_for_interval([1,2,3,5,7,9],1)
		assert(_index == 0 and _count == 3)	

	def test_find_longest_count_nowrap_entirescale(self):
		_index, _count = music.find_longest_count_for_interval([1,3,5,7,9,11],2)
		assert(_index == 0 and _count == 6)	

	def test_find_longest_count_wrapping_entirescale(self):
		_index, _count = music.find_longest_count_for_interval([1,3,7,9,11],2)
		assert(_index == 2 and _count == 5)	

	def test_find_longest_count_wrapping_is_longest(self):
		_index, _count = music.find_longest_count_for_interval([1,2,3,5,6,7,8,11,12],1)
		assert(_index == 7 and _count == 5)	

	def test_find_longest_count_wrapping_is_not_longest(self):
		_index, _count = music.find_longest_count_for_interval([1,3,5,6,7,8,11,12],1)
		assert(_index == 2 and _count == 4)	

	def test_find_longest_count_wrapping_starts_at_last_element(self):
		_index, _count = music.find_longest_count_for_interval([10, 12, music.MINUS_MASK, music.MINUS_MASK, music.MINUS_MASK, 8], 2)
		assert(_index == 5 and _count == 3)

	def test_find_longest_count_wrapping_starts_second_to_last_element(self): 
		_index, _count = music.find_longest_count_for_interval([10, 12, music.MINUS_MASK, music.MINUS_MASK, 6, 8], 2)
		assert(_index == 4 and _count == 4)

	##### find_scale_components #####

	def test_find_scale_components(self):
		scale = [1,2,3]
		interval = 1
		results = music.find_scale_components(scale, interval)
		assert(len(results) == 1)
		assert(results[0]['len_chunk'] == 3)
		assert(results[0]['index'] == 0)

	def test_find_scale_components_twice(self):
		scale=[1,2,3,5,6,7]
		interval = 1
		repeat = 2
		results = music.find_scale_components(scale, interval, repeat)
		assert(len(results) == 2)
		assert(results[0]['interval'] == 1)
		assert(results[0]['len_chunk'] == 3)
		assert(results[0]['index'] == 0)
		assert(results[1]['interval'] == 1)
		assert(results[1]['len_chunk'] == 3)
		assert(results[1]['index'] == 3)

	##### fetch_scale_components #####

	def test_fetch_scale_components_major_scale(self):
		scale = music.convert_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])
		list_of_intervals = [3,3,3,2,2,1]
		results = music.fetch_scale_components(list_of_intervals, scale)
		assert(len(results) == 2)
		assert(results[0]['interval'] == 2)
		assert(results[0]['len_chunk'] == 4)
		assert(results[0]['index'] == 3)
		assert(results[1]['interval'] == 2)
		assert(results[1]['len_chunk'] == 3)
		assert(results[1]['index'] == 0)

	def test_fetch_scale_components_major_scale(self):
		scale = music.convert_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])
		list_of_intervals = [3,3,3,2,2,1]
		results = music.fetch_scale_components(list_of_intervals, scale)
		assert(len(results) == 2)
		assert(results[0]['interval'] == 2)
		assert(results[0]['len_chunk'] == 4)
		assert(results[0]['index'] == 3)
		assert(results[1]['interval'] == 2)
		assert(results[1]['len_chunk'] == 3)
		assert(results[1]['index'] == 0)

	# def test_fetch_scale_components_minor_scale(self):
	# 	scale = music.convert_scale(['C', 'D', 'EFLAT', 'F', 'G', 'AFLAT', 'B', 'C'])
	# 	list_of_intervals = [3,3,3,2,2,1]
	# 	results = music.fetch_scale_components(list_of_intervals, scale)
	# 	assert(len(results) == 3)
	# 	assert(results[0]['interval'] == 3)
	# 	assert(results[0]['len_chunk'] == 2)
	# 	assert(results[0]['index'] == 5)
	# 	assert(results[1]['interval'] == 2)
	# 	assert(results[1]['len_chunk'] == 3)
	# 	assert(results[1]['index'] == 2)		
	# 	assert(results[2]['interval'] == 2)
	# 	assert(results[2]['len_chunk'] == 2)
	# 	assert(results[2]['index'] == 0)

if __name__ == '__main__':
	unittest.main()
	print("Finished running tests")




