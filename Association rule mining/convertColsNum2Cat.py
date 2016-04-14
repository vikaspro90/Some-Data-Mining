import numpy as np

def main():
	cols2Convert = [1,4] # provide the column numbers(not indices) that are numerical
	fileName = "cmc\\cmc.data"
	data = np.genfromtxt(fileName, delimiter=',', dtype = int)
	rows, columns = np.shape(data)
	for col in cols2Convert:
		ind = col - 1
		# we will divide the range into 3
		mark1 = np.sort(data[:,ind])[rows/3]
		mark2 = np.sort(data[:,ind])[2 * rows/3]
		print rows, mark1, mark2
		print len(data[:,ind][data[:,ind] < mark1]), len(data[:,ind][np.all([data[:,ind] >= mark1, data[:,ind] < mark2], axis = 0)]), len(data[:,ind][data[:,ind] >= mark2])
		data[:,ind][data[:,ind] < mark1] = 0
		data[:,ind][np.all([data[:,ind] >= mark1, data[:,ind] < mark2], axis = 0)] = 1
		data[:,ind][data[:,ind] >= mark2] = 2
		print len(data[:,ind][data[:,ind]==0]), len(data[:,ind][data[:,ind]== 1]), len(data[:,ind][data[:,ind] == 2])
		np.savetxt("cmc\\cmcOriginal.txt", data, delimiter=',', fmt = '%1.0f')
if __name__ == "__main__":
	main()