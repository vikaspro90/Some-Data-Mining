# Author 		: Vikas Palakurthi
# Last modified	: Mar 2016

# This function takes a file with a single record to be classified and a file with the training data as arguments.
import sys
# import numpy as np

def predictClass(data, dTree):
	key = dTree.keys()[0]
	while key[0] != 1:
		c = key[2]
		v = key[3]
		if float(data[c]) > v:
			x = 'g'
		else:
			x = 'l'
		children = dTree[key]
		for child in children.keys():
			if child[1] == x:
				key = child
		dTree = children
	return dTree[key]

def main():
	if len(sys.argv) < 3:
		print "This function takes a file with a single record to be classified and a file with the training data as arguments. Terminating..."
		sys.exit(0)

	dataFile = open(sys.argv[1], 'r')
	data = dataFile.readline().split(',')
	dataFile.close()

	inp = sys.argv[2]
	inpFile = open(inp, 'r')
	numInp = len(inpFile.readline().split(','))
	if numInp-1 != len(data):
		print "The test file and training file have incompatible number of columns. Terminating..."
		sys.exit(0)
	treeFileName = "Decision tree for " + inp.replace('.',' ') + ".txt"
	try:
		treeFile = open(treeFileName, 'r')
	except:
		print "Failed to open the tree file", treeFileName, "Terminating..."
		sys.exit(0)
	dTree = eval(treeFile.readline().strip())

	label = predictClass(data, dTree)
	print "The input data belongs to class:", label

if __name__ == "__main__":
	main()