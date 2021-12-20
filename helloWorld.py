import sys

def hello(name):
	print(f'Hello {name}')
	
def main():
	name = str(sys.argv[1])
	hello(name)
	
main()