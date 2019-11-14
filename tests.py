import unittest
import music
import musicenums

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

	##### find_longest_chunk ######

	def test_find_longest_chunk_empty(self):
		_index, _chunk = music.find_longest_chunk([], 1)
		assert (_chunk == 1)

	def test_find_longest_chunk_at_beginning(self):
		scale = [1,2,3,4,5,7,10]
		_index, _chunk = music.find_longest_chunk(scale, 1)
		assert (_index == 0 and _chunk == 5)

	def test_find_longest_chunk_at_end(self):
		scale = [1,2,7,9,11,13]
		_index, _chunk = music.find_longest_chunk(scale, 2)
		assert (_index == 2 and _chunk == 4)

	def test_find_longest_chunk_wrapping_loop(self):
		scale = [1,3,7,9,11]
		_index, _chunk = music.find_longest_chunk(scale, 2)
		assert (_index == 2 and _chunk == 5)

	def test_find_longest_chunk_wrapping_notloop(self):
		scale = [1,2,3,7,9,11]
		_index, _chunk = music.find_longest_chunk(scale, 2)
		assert (_index == 3 and _chunk == 4)

	##### find_scale_components #####

	def test_find_scale_components(self):
		scale = [1,2,3]
		interval = 1
		results = music.find_scale_components(interval, scale)
		assert(len(results) == 1)
		assert(results[0]['len_chunk'] == 3)
		assert(results[0]['index'] == 0)

	def test_find_scale_components_twice(self):
		scale=[1,2,3,5,6,7]
		interval = 1
		repeat = 2
		results = music.find_scale_components(interval, scale, repeat)
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

	def test_fetch_scale_components_minor_scale(self):
		scale = music.convert_scale(['C', 'D', 'EFLAT', 'F', 'G', 'AFLAT', 'B', 'C'])
		list_of_intervals = [3,3,3,2,2,1]
		results = music.fetch_scale_components(list_of_intervals, scale)
		assert(len(results) == 3)
		assert(results[0]['interval'] == 3)
		assert(results[0]['len_chunk'] == 2)
		assert(results[0]['index'] == 5)
		assert(results[1]['interval'] == 2)
		assert(results[1]['len_chunk'] == 3)
		assert(results[1]['index'] == 2)		
		assert(results[2]['interval'] == 2)
		assert(results[2]['len_chunk'] == 2)
		assert(results[2]['index'] == 0)

if __name__ == '__main__':
	unittest.main()
	print("Finished running tests")




