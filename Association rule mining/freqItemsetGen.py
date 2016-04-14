import sys
import datetime
import numpy as np
import itertools

def bruteForce(k):
	global numItems
	nextSet = set([])
	# create all possible k-combinations of all the codes present
	for combo in itertools.combinations(range(numItems), k):
		nextSet.add(frozenset(combo))
	return nextSet

def Fkminus1xF1(k):
	nextSet = set([])
	for itemset in F[k-1]:
		for item in F[1]:
			if not item.issubset(itemset):
				nextSet.add(itemset.union(item))
	return list(nextSet)

def Fkminus1xFkminus1(k):
	nextSet = set([])
	for one, two in itertools.combinations(F[k-1], 2):
		# we need to compare first k-2 elements
		if sorted(list(one))[:k-2] == sorted(list(two))[:k-2]:
			nextSet.add(one.union(two))
	return list(nextSet)

def aprioriGen(k, itemChoice):
	if itemChoice.lower() == 'b':
		return bruteForce(k)
	elif itemChoice.lower() == 'f1':
		return Fkminus1xF1(k)
	elif itemChoice.lower() == 'fk':
		return Fkminus1xFkminus1(k)
	else:
		print "Invalid choice entered for itemset generation method. Choose from 'b', 'f1' and 'fk'. Terminating..."
		sys.exit(-1)

def apriori(minsup, data, fileName, itemChoice):
	global F # F is a dictionary for key(level) : value(list of itemSETS at that level)
	global numItems # Total number of unique codes in data
	global numTrans # Total number of transactions
	msgFmt = "{0:>2} {1:>10} {2:>10}" # some output formatting
	header = ('k', 'Candidate', 'Frequent')
	k = 1
	F[k] = [] # so F[k] will be a list of sets
	support = {}
	support[k] = {}
	numTrans, numItems = np.shape(data)
	for itemset in np.where((data.sum(axis=0)/float(numTrans)) >= minsup)[0]:
		F[k].append(frozenset({itemset}))
		support[k][frozenset({itemset})] = data[:,itemset].sum(axis=0)/float(numTrans)
	totNumC = numItems
	totNumF = len(F[k])
	nummf = 0 # number of maximal frequent itemsets
	numcf = 0 # number of closed frequent itemsets
	msg = [(str(k), str(totNumC), str(totNumF))]
	while len(F) == k:
		k = k+1
		Ck = aprioriGen(k, itemChoice) # should return a list of frozen sets. We send k, but k-1 will be used in the function
		numC = len(Ck)
		totNumC += numC
		support[k] = {}
		for row in data:
			T = set(np.where(row==1)[0]) # T should represent set of indices of 1s in the row
			Ct = [sub for sub in Ck if sub.issubset(T)] # members of Ck that are in T will be a list of sets
			for itemset in Ct:
				if itemset in support[k]:
					support[k][itemset] += 1
				else:
					support[k][itemset] = 1
		F[k] = []
		for itemset in support[k].keys():
			supp = float(support[k][itemset])/numTrans
			if supp >= minsup:
				F[k].append(itemset)
				support[k][itemset] = supp
			else:
				del support[k][itemset]

		if len(F[k]) == 0:
			del F[k]
			del support[k]
			numF = 0
		else:
			numF = len(F[k])
		totNumF += numF
		msg.append((str(k), str(numC), str(numF)))

		# Below code is to count the maximal and closed frequent itemsets
		if k in F:
			for curr in F[k-1]:
				cf = True
				mf = True
				for next in F[k]:
					if curr.issubset(next):
						if support[k-1][curr] == support[k][next]: # This means that curr is not a closed set
							cf = False
							mf = False # if curr is not closed, then it is definitely not maximal
							break
						mf = False # cannot break now as we still have to confirm that curr is not closed
				if mf == True: # curr is a maximal frequent itemset as it has no immediate superset which is frequent.
					nummf += 1
				if cf ==  True:
					numcf += 1
		else:
			nummf += len(F[k-1])
			numcf += len(F[k-1])

	logFile = open(fileName.split('.')[0]+"LOG"+".txt", 'a')
	# Uncomment below 2 lines to print all frequent itemsets==================
	# print "Below are all the frequent itemsets with a minimum support of", minsup, "\n"
	# print F	# F[k] should be a subset of Ck where count > minsup
	logFile.write("Timestamp: "+str(datetime.datetime.now())+"\n")
	logFile.write("Minimum support: "+str(minsup))
	print "\n", msgFmt.format(*header)
	logFile.write("\n" + msgFmt.format(*header) + "\n")
	print '-' * 24
	logFile.write('-' * 24 + "\n")
	for i in msg:
		print msgFmt.format(*i)
		logFile.write(msgFmt.format(*i)+"\n")
	print '-' * 24
	logFile.write('-' * 24 + "\n")
	print msgFmt.format(" ", str(totNumC), str(totNumF))
	logFile.write(msgFmt.format(" ", str(totNumC), str(totNumF)) + "\n")
	print '-' * 24, "\n"
	logFile.write('-' * 24 + "\n")
	print "Total number of frequent itemsets:        ", str(totNumF)
	logFile.write("Total number of frequent itemsets:        " + str(totNumF) + "\n")
	print "Total number of closed frequent itemsets: ", str(numcf)
	logFile.write("Total number of closed frequent itemsets: " + str(numcf) + "\n")
	print "Total number of maximal frequent itemsets:", str(nummf), "\n"
	logFile.write("Total number of maximal frequent itemsets:" + str(nummf) + "\n")
	logFile.close()
	return F, support

F = {}
numItems = 0
numTrans = 0

def main():
	inpName = "cars\\carBinary.txt"
	data = np.genfromtxt(inpName, dtype=int, delimiter=',')
	minsup = 0.3
	apriori(minsup, data, inpName, 'b')

if __name__ == "__main__":
	start = datetime.datetime.now()
	main()
	print "\nTotal execution time:", (datetime.datetime.now() - start).total_seconds(), "seconds"