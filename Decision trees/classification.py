# Author 		: Vikas Palakurthi
# Last modified	: Mar 2016

import sys
from collections import Counter
import numpy as np
import math

# The below function finds the gini for each column
def findWeightedGini(dataAtNode, c, clsInd):
	allVals = dataAtNode[:,c].astype(float)
	allValsUniq = np.unique(allVals)
	numVals = len(allValsUniq)
	bestg = float("inf")
	bestv = None
	for i in range(1, numVals):
		mid = float((allValsUniq[i-1] + allValsUniq[i])/2)
		moreThanMid = len(allVals[allVals > mid])
		lessThanMid = len(allVals[allVals <= mid])
		g1 = 1
		g2 = 1
		# for l in set(dataAtNode[:,dataAtNode.shape[1]-1]):
		for l in set(dataAtNode[:,clsInd]):
			# calculating the gini.
			if moreThanMid == 0:
				g1 -= 0
			else:
				g1 -= (float(len(dataAtNode[np.logical_and(dataAtNode[:,c].astype(float) > mid, dataAtNode[:,clsInd] == l)]))/moreThanMid) ** 2
			if lessThanMid == 0:
				g2 -= 0
			else:
				g2 -= (float(len(dataAtNode[np.logical_and(dataAtNode[:,c].astype(float) <= mid, dataAtNode[:,clsInd] == l)]))/lessThanMid) ** 2
		g = float((moreThanMid * g1) + (lessThanMid * g2))/numVals
		if g < bestg:
			bestg = g
			bestv = mid
	return bestg, bestv

# The below function finds the entropy.
def findInfoGain(dataAtNode, c, clsInd):
	allVals = dataAtNode[:,c].astype(float)
	allValsUniq = np.unique(allVals)
	numVals = len(allValsUniq)
	beste = float("inf")
	bestv = None
	for i in range(1, numVals):
		mid = float((allValsUniq[i-1] + allValsUniq[i])/2)
		moreThanMid = len(allVals[allVals > mid])
		lessThanMid = len(allVals[allVals <= mid])
		e1 = 0
		e2 = 0
		# for l in set(dataAtNode[:,dataAtNode.shape[1]-1]):
		for l in set(dataAtNode[:,clsInd]):
			# calculating the entropy.
			if moreThanMid == 0:
				e1 -= 0
			else:
				p = float(len(dataAtNode[np.logical_and(dataAtNode[:,c].astype(float) > mid, dataAtNode[:,clsInd] == l)]))/moreThanMid
				if p > 0:
					e1 -= p * math.log(p, 2)
				else:
					e1 = 0
			if lessThanMid == 0:
				e2 -= 0
			else:
				p = float(len(dataAtNode[np.logical_and(dataAtNode[:,c].astype(float) <= mid, dataAtNode[:,clsInd] == l)]))/lessThanMid
				if p > 0:
					e2 -= p * math.log(p, 2)
				else:
					e2 = 0
		e = float((moreThanMid * e1) + (lessThanMid * e2))/numVals
		if e < beste:
			beste = e
			bestv = mid
	return beste, bestv

def bestSplit(dataAtNode, measure, cls, ignore):
	clsInd = cls - 1
	best = (0, float("inf"), None)
	for c in range(dataAtNode.shape[1]-1):
		if (c == clsInd) or (c+1 in ignore):
			continue
		if measure == 'g':
			m, v = findWeightedGini(dataAtNode, c, clsInd) #should return which gini and which value to split at
		else:
			m, v = findInfoGain(dataAtNode, c, clsInd) #should return which entropy and which value to split at
		if m < best[1]:
			best = (c, m, v)
	# if best[0] == clsInd:
	# print best[1], best[2]
	return best

def build(data, tree, x, measure, cls, ignore):
	flag = True
	for col in range(data.shape[1]-1):
		if col == cls - 1:
			continue
		if len(set(data[:,col])) != 1:
			flag = False
			break
	# condition 1 is when there is just one class in the dataset
	# condition 2 is when all rows in the dataset have same feature values
	if (len(set(data[:,cls-1])) == 1) or flag:
		if flag:
			leaf = {(1, x):Counter(data[:,cls-1]).most_common(1)[0][0]}
		else:
			leaf = {(1, x):data[0,cls-1]} # x is to make the keys unique for two children
		# print leaf
		return leaf
	else:
		c, g, v = bestSplit(data, measure, cls, ignore)
		tree[(0, x, c, v)] = {}
		dataG = data[data[:,c].astype(float) > v]
		dataL = data[data[:,c].astype(float) <= v]
		childG = build(dataG, tree[(0, x, c, v)], 'g', measure, cls, ignore)
		childL = build(dataL, tree[(0, x, c, v)], 'l', measure, cls, ignore)
		tree[(0, x, c, v)][childG.keys()[0]] = childG.values()[0]
		tree[(0, x, c, v)][childL.keys()[0]] = childL.values()[0]
		return tree

def buildTree(data, measure, cls, ignore = []):
	tree = build(data, {}, 'r', measure, cls, ignore)
	return tree

def main():
	# measure = raw_input("Please choose one of the below measures to use for choosing an attribute to split in every step...\ng for Gini\ni for information gain\n:").strip().lower()
	measure = 'g'
	while measure not in 'ig':
		measure = raw_input("Wrong option chosen. Choose from the below options...\ng for Gini\ni for information gain\n:").strip().lower()
	# read the training dataset
	filename = "data.txt"
	data = np.genfromtxt(filename, delimiter=',', dtype = str)
	# build a decision tree
	cls = 4 # last column of the data
	dTree = buildTree(data, 'g', cls, [])
	treeFileName = "Decision tree for " + filename.replace('.',' ') + ".txt"
	treeFile = open(treeFileName, 'w')
	treeFile.write(str(dTree))
	treeFile.close()
	print dTree

if __name__ == "__main__":
	main()