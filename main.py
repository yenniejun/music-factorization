import music

def get_outputs(scale):
	outputs=[]
	outputs.append(music.fetch_scale_components([5,4,3,3,3,2,2,1], scale))
	outputs.append(music.fetch_scale_components([4,3,3,3,2,2,1], scale))
	outputs.append(music.fetch_scale_components([3,3,3,2,2,1], scale))
	outputs.append(music.fetch_scale_components([2,1],scale))
	return outputs

def print_outputs(outputs):
	print("----")
	for output in outputs:
		music.print_results(output)
		print("----")
		### Need to detect repeats

def main():
	my_input = list(map(str, input("Describe your scale using letters separated by a space:\n").split())) 
	scale = music.convert_scale([a.upper() for a in my_input])
	outputs = get_outputs(scale)
	print_outputs(outputs)
	

if __name__ == "__main__":
	main()