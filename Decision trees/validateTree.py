# Author 		: Vikas Palakurthi
# Last modified	: Mar 2016

import sys
import numpy as np
import splitFile
import classification
import prediction
import datetime

def main():
	dataset = "datasets"
	fileName = dataset+"\\"+"iris.txt"
	delim = ','
	trainData = np.genfromtxt(fileName, delimiter=delim, dtype=str)
	cols = len(trainData[0])
	cls = cols
	clsInd = cls - 1
	ignore = [] # must be a list of columns(not indices) that are to excluded from calculations of gini, or just use empty list
	measure = raw_input("Please choose one of the below measures to use for choosing an attribute to split in every step...\ng for Gini\ni for information gain\n:").strip().lower()
	while measure not in 'ig':
		measure = raw_input("Wrong option chosen. Choose from the below options...\ng for Gini\ni for information gain\n:").strip().lower()
	print "Splitting File...."+fileName
	subFiles = splitFile.splitFile(fileName, 10)
	numTests = 0
	correct = 0
	print "Starting 10 fold cross validation...."
	for k in range(10):
		test = subFiles[k]
		train = subFiles[:k]+subFiles[k+1:]
		trainData = np.genfromtxt(train[0], delimiter=delim, dtype=str)
		for t in range(1, len(train)):
			trainData = np.append(trainData, np.genfromtxt(train[t], delimiter=delim, dtype = str), axis = 0)

		dTree = classification.buildTree(trainData,measure, cls, ignore) # cls is the column number of the class label(column number, not index of column)
																# ignore is optional
		testData = np.genfromtxt(test, delimiter=delim,dtype=str)
		for i in range(len(testData)):
			label = prediction.predictClass(testData[i], dTree)
			if label.strip() == testData[i][clsInd].strip():
				correct += 1
			numTests += 1
		print k+1, "iteration(s) done...."
	accuracy = float(correct)*100/(numTests)
	accMsg = "Accuracy:\t"+str(round(accuracy,2))+'%'
	logFile = open("k-fold log.txt", 'a')
	logFile.write("File Name:\t"+fileName+'\n'+"Sub Files:\t"+", ".join(subFiles)+'\n'+"Class at:\t"+str(cls)+'\n'+"Ignore cols:\t"+str(ignore)+'\n'+"Measure:\t"+measure+'\n'+accMsg+'\n'+"Timestamp:\t"+str(datetime.datetime.now())+'\n'+'-'*150+'\n')
	logFile.close()
	print accMsg

if __name__ == "__main__":
	start = datetime.datetime.now()
	main()
	print "Total execution time:", (datetime.datetime.now() - start).total_seconds(), "seconds"