import sys
import numpy as np
import datetime
import itertools
import freqItemsetGen

def nextGen(m):
	global H
	nextSet = set([])
	for itemset in H[m-1]:
		for item in H[1]:
			if not item.issubset(itemset):
				nextSet.add(itemset.union(item))
	return list(nextSet)

def genRules():
	global H
	global support
	global minconf
	global minlift
	rules = []

	for k in F.keys():
		if k >= 2:
			for itemset in F[k]:
				m = 1
				H[m] = [frozenset([x]) for x in itemset]
				while k > m:
					bad = []
					for consequent in H[m]:
						antecedent = itemset - consequent
						confidence = support[k][itemset]/support[k-m][antecedent]
						if confidence >= minconf:
							rules.append((confidence, antecedent, consequent))
						else:
							bad.append(consequent)
					for c in bad:
						H[m].remove(c)
					m += 1
					H[m] = nextGen(m)
	return rules

def genRulesBrute():
	global H
	global support
	rules = []
	for k in F.keys():
		if k >= 2:
			for itemset in F[k]:
				for x in range(1, k):
					for combo in itertools.combinations(itemset, x):
						consequent = frozenset(combo)
						antecedent = itemset - consequent
						lift = support[k][itemset]/(support[k-x][antecedent] * support[x][consequent])
						if lift >= minlift:
							rules.append((lift, antecedent, consequent))
	return rules

H = {}
F = {}
support = {}
minconf = 0
minlift = 0

def main():
	global minconf
	global minlift
	global F
	global support
	print len(sys.argv)
	print sys.argv
	if len(sys.argv) < 7:
		print "Not enough arguments. Refer to the readme. Terminating..."
		sys.exit(-1)
	minsup = float(sys.argv[3])
	minimum = float(sys.argv[6])
	inpName = sys.argv[1]
	data = np.genfromtxt(inpName, dtype=int, delimiter=',')
	F, support = freqItemsetGen.apriori(minsup, data, inpName, sys.argv[4])
	# Set whether you want the confidence or lift as interestingness measure.=
	choice = sys.argv[5] # should either be c or l
	# ========================================================================
	if choice.lower() == 'c':
		measure = "confidence"
		minconf = minimum
		rules = genRules()
	elif choice.lower() == 'l':
		measure = "lift"
		minlift = minimum
		rules = genRulesBrute()
	else:
		print "Invalid choice entered for interestingness measure. Refer to readme. Terminating..."
		sys.exit(-1)
	numRules = len(rules)
	logFile = open(inpName.split('.')[0]+"LOG"+".txt", 'a')
	if numRules > 0:
		print "Below are the", numRules, "association rules with a", measure, "of atleast", minimum, ":\n"
	else:
		print "No rules could be formed with minimum " + measure + " of " + str(minimum) + ". Try decreasing the value."
	logFile.write("Minimum " + measure + ": " + str(minimum) + '\n')
	logFile.write("Number of association rules generated: " + str(numRules) + '\n')
	# provide the columns file below. Each column must be like originalColumnName:uniqueValue
	columnsFile = open(sys.argv[2],'r')
	columns = columnsFile.read().strip().split(',')
	columnsFile.close()
	# Uncomment the below lines are to print all rules==================================
	# for a in rules:
	# 	print list(a[1]), "--->", list(a[2])
	# for a in rules:
	# 	print [columns[int(item)] for item in a[1]], "--->", [columns[int(cons)] for cons in a[2]]
	# The below lines are to print top 10 rules==================================
	print "Below are the top 10 rules generated:"
	for a in sorted(rules, reverse=True)[:10]:
		print [columns[int(item)] for item in a[1]], "--->", [columns[int(cons)] for cons in a[2]], "\t", measure, a[0]
	logFile.write('*'*150+'\n'+'\n')
	logFile.close()

if __name__ == "__main__":
	start = datetime.datetime.now()
	main()
	print "\nTotal execution time:", (datetime.datetime.now() - start).total_seconds(), "seconds"