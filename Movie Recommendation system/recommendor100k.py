# Author 		: Vikas Palakurthi
# IU username	: vpalakur
# Last modified	: Feb 2016

import numpy as np
from scipy.spatial import distance
import time
import sys

def calcDistances(userMovArray, uniqUserList, seenMov, userInfo, avgRating, userStd, met):
	distMat = np.empty((np.shape(userMovArray)[0], np.shape(userMovArray)[0]), float)
	distMat.fill(float("inf"))
	if met == 'e':
		metric = 'euclidean'
	elif met == 'm':
		metric = 'cityblock'
	elif met == 'l':
		metric = 'chebyshev'
	elif met == 'c':
		metric = 'cosine'
	elif met == 'h':
		metric = 'hamming'
	func = getattr(distance, metric)

	for i in uniqUserList:
		for j in uniqUserList[uniqUserList != i]:
			commonMov = np.intersect1d(seenMov[str(int(i))], seenMov[str(int(j))], assume_unique=True)
			if len(commonMov) > 0:
				user1 = userMovArray[i, commonMov]
				user1 = (user1 - avgRating[str(int(i))])/userStd[str(int(i))]
				user2 = userMovArray[j, commonMov]
				user2 = (user2 - avgRating[str(int(j))])/userStd[str(int(j))]
				if  userInfo[str(int(i))]['gender'] == userInfo[str(int(j))]['gender']:
					if  abs(userInfo[str(int(i))]['age'] - userInfo[str(int(j))]['age']) <= 5:
						distMat[int(i), int(j)] = func(user1, user2) * 0.5
					elif abs(userInfo[str(int(i))]['age'] - userInfo[str(int(j))]['age']) <= 10:
						distMat[int(i), int(j)] = func(user1, user2) * 0.6
					elif abs(userInfo[str(int(i))]['age'] - userInfo[str(int(j))]['age']) <= 15:
						distMat[int(i), int(j)] = func(user1, user2) * 0.7
					elif abs(userInfo[str(int(i))]['age'] - userInfo[str(int(j))]['age']) <= 20:
						distMat[int(i), int(j)] = func(user1, user2) * 0.8
					else:
						distMat[int(i), int(j)] = func(user1, user2) * 0.9
				else:
					if  abs(userInfo[str(int(i))]['age'] - userInfo[str(int(j))]['age']) <= 5:
						distMat[int(i), int(j)] = func(user1, user2) * 0.6
					elif abs(userInfo[str(int(i))]['age'] - userInfo[str(int(j))]['age']) <= 10:
						distMat[int(i), int(j)] = func(user1, user2) * 0.7
					elif abs(userInfo[str(int(i))]['age'] - userInfo[str(int(j))]['age']) <= 15:
						distMat[int(i), int(j)] = func(user1, user2) * 0.8
					elif abs(userInfo[str(int(i))]['age'] - userInfo[str(int(j))]['age']) <= 20:
						distMat[int(i), int(j)] = func(user1, user2) * 0.9
					else:
						distMat[int(i), int(j)] = func(user1, user2)
	return distMat

def findSimilar(uniqUserList, distMat):
	similarUsersDict = {}
	for u in uniqUserList.__iter__():
		similarUsers = distMat[int(u)].ravel().argsort() # returns the indices of distance matrix in the increasing
													# order of the values at the indices. So closest users come first.
		similarUsers = similarUsers[similarUsers != 0] # removes userID 0.
		similarUsersDict[str(int(u))] = similarUsers[similarUsers != int(u)]
	return similarUsersDict

def calcMad(testFileArray, similarUsersDict, userMovArray, avgRating, distMat, sim):
	dTot = 0
	rTot = 0
	for row in testFileArray:
		user = int(row[0])
		movie = int(row[1])
		t = float(row[2])
		k = sim
		if user >= userMovArray.shape[0] or movie >= userMovArray.shape[1]:
			print "Prediction not made for the user {} movie {} pair as data about either of them was not available".format(user, movie)
			continue
		friends = []
		if len(similarUsersDict[str(user)]) > k:
			for item in similarUsersDict[str(user)]:
				if userMovArray[item, movie] > 0.0:
					friends.append(item)
					k -= 1
				if k == 0:
					break
			count = len(friends)
		else:
			for item in similarUsersDict[str(user)]:
				if userMovArray[item, movie] > 0.0:
					friends.append(item)
			count = len(friends)
		if count == 0:
			r = 0
			t = 0
			p = 0
		else:
			numerator = 0.0
			for x in friends:
				numerator = numerator + (userMovArray[x, movie] - avgRating[str(x)])
			p = avgRating[str(user)] + numerator/count
			r = 1
		dTot += r * abs(p - t)
		rTot += r
	return dTot, rTot

def main():
	print "Choose a distance metric to use\n", "\n".join(["e for euclidean", "m for manhattan", "l for LMax"])
	met = raw_input(":")
	if met.lower() not in ['e', 'm', 'l', 'c', 'h']:
		print "Invalid metric chosen. Terminating."
		sys.exit(0)
	sim = input("Enter number of similar users to consider: ")

	baseFileList = ["D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u1.base", "D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u2.base", "D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u3.base", "D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u4.base", "D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u5.base"]
	testFileList = ["D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u1.test", "D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u2.test", "D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u3.test", "D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u4.test", "D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u5.test"]
	userInfoFile = "D:\\Study\\MS in CS\\Spring 2016\\Data Mining\\assignments\\hw1\\ml-100k\\u.user"
	delimiter = "\t"
	finalD = 0.0
	finalR = 0.0
	userInfoArray = np.genfromtxt(userInfoFile, delimiter = "|", usecols=(0, 1, 2), dtype = str)
	for baseFile in baseFileList:
		baseFileArray = np.genfromtxt(baseFile, delimiter = delimiter, usecols=(0, 1, 2), dtype = float)
		uniqUserList = np.unique(baseFileArray[:,0])
		uniqMovieList = np.unique(baseFileArray[:,1])
		testFile = testFileList[baseFileList.index(baseFile)]
		testFileArray = np.genfromtxt(testFile, delimiter = delimiter, usecols=(0, 1, 2), dtype = float)

		print "Fetching info ..."
		numUsers = int(np.max(baseFileArray[:,0]))
		numMovies = int(np.max(baseFileArray[:,1]))

		print "Loading base file data..."
		userMovArray = np.zeros((numUsers+1, numMovies+1))
		for row in baseFileArray:
			userMovArray[int(row[0]), int(row[1])] = row[2]

		print "Loading user information..."
		userInfo = {}
		for row in userInfoArray:
			userInfo[row[0]] = {'age':int(row[1]), 'gender':row[2]}

		print "Loading movies seen by users and average ratings of users..."
		seenMov = {}	# stores the movies rated by each user
		avgRating = {}	# stores average rating of each user
		userStd = {}	# stores the standard deviation of ratings by each user
		userMovArrayCopy = np.copy(userMovArray)
		userMovArrayCopy[userMovArrayCopy == 0] = np.nan
		for user in uniqUserList.__iter__():
			seenMov[str(int(user))] = np.where((userMovArray[user] > 0))[0]
			avgRating[str(int(user))] = np.sum(userMovArray[user])/np.count_nonzero(userMovArray[user])
			userStd[str(int(user))] = np.nanstd(userMovArrayCopy[user])

		print "Calculating distance matrix.."
		distMat = calcDistances(userMovArray, uniqUserList, seenMov, userInfo, avgRating, userStd, met)

		print "Building similar users for all users..."
		similarUsersDict = findSimilar(uniqUserList, distMat)

		print "Started performance test..."
		dTot, rTot = calcMad(testFileArray, similarUsersDict, userMovArray, avgRating, distMat, sim)
		print "The MAD for test file {} is found out to be:".format(testFileList.index(testFile)+1), dTot/rTot
		finalD += dTot
		finalR += rTot

	print "The final MAD over all test files is calculated to be:", finalD/finalR

if __name__ == "__main__":
	start_time = time.time()
	main()
	print "Executed in {} seconds".format(time.time() - start_time)