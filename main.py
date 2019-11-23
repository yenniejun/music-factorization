import music

def get_outputs(scale):
	outputs=[]
	outputs.append(music.fetch_scale_components([4,4,4,4,3,3,3,2,2,1], scale))
	outputs.append(music.fetch_scale_components([3,3,3,2,2,1], scale))
	outputs.append(music.fetch_scale_components([2,2,1], scale))
	outputs.append(music.fetch_scale_components([1],scale))
	return validate_outputs(outputs)

def convert_set_to_dict(s1):
	d1 = []
	while s1:
		d1.append(dict(s1.pop()))
	return d1

def validate_outputs(outputs):
	cleaned = []
	masterset = []
	for output in outputs:
		if(len(output) != 0):
			s1 = set()
			for dic in output:
				s1.add(tuple(dic.items()))
			if s1 not in masterset:
				masterset.append(s1)
				cleaned.append(convert_set_to_dict(s1.copy()))
	return cleaned


def print_outputs(outputs):
	print("----")
	for output in outputs:
		music.print_results(output)
		print("----")

def main():
	my_input = list(map(str, input("Describe your scale using letters separated by a space:\n").split())) 
	scale = music.convert_scale([a.upper() for a in my_input])
	outputs = get_outputs(scale)
	print_outputs(outputs)
	

if __name__ == "__main__":
	main()