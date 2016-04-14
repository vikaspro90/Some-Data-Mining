import numpy as np

def main():
	columnsFile = open("cmc\\cmcOriginalCols.txt", 'r')
	fileName = "cmc\\cmcOriginal.txt"
	columns = columnsFile.read().strip().split(',')
	columnsFile.close()
	data = np.genfromtxt(fileName, delimiter=',', dtype = str)
	print data
	uniq = {}
	r_orig, c_orig = np.shape(data)
	rows = r_orig
	cols = 0
	for i in range(c_orig):
		uniq[i] = tuple(np.unique(data[:,i])) # dictionary of {column : list of unique values in that column}
		cols += len(uniq[i]) # will be the number of columns in the sparse matrix
	print uniq
	sparse = np.zeros((rows, cols))
	id = 0
	headers = []
	for c in range(c_orig):
		for val in uniq[c]:
			for spot in np.where(data[:, c] == val): # spot gives the row indices of where val is
				sparse[spot, id] = 1
			headers.append(':'.join([columns[c], val]))
			id += 1
	np.savetxt("cmc\\cmcBinary.txt", sparse, delimiter=',', fmt = '%1.0f')
	columnsFile = open("cmc\\cmcColumns.txt", 'w')
	columnsFile.write(','.join(headers))
	columnsFile.close()
if __name__ == "__main__":
	main()