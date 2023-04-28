import sys

from read_input import read_input

def main():
	if(len(sys.argv) <= 2):
		print("Invalid input")
		return
	else:
		method = sys.argv[1]
		file_name = sys.argv[2]
		read_input(file_name)
main()