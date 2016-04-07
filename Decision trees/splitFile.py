# Author 		: Vikas Palakurthi
# Last modified	: Mar 2016

import sys
import numpy as np

def splitFile(fileName, numFolds):
	file = open(fileName, 'r')
	fileData = file.readlines()
	file.close()
	length = len(fileData)

	subsetSize = length/numFolds
	subFiles = []
	for i in range(numFolds):
		temp = fileName.split('.')
		subFileName = temp[0]+str(i)+'.'+temp[1]
		subFiles.append(subFileName)
		skip = i*subsetSize
		if skip + subsetSize <= length:
			subData = fileData[skip:skip+subsetSize]
		else:
			subData = file[skip:]
		subFile = open(subFileName, 'w')
		subFile.writelines(subData)
		subFile.close()
	return subFiles

def main():
	fileName = 'iris.txt'
	subFiles = splitFile(fileName, 10)


if __name__ == "__main__":
	main()