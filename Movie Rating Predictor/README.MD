This is a straight forward movie rating prediction system that tries to predict the rating a user may give to a certain movie. This is achieved using collaborative filtering. We first find the K nearest neighbors(commonly known as KNN) based on the similarities between current user's ratings, and other users' ratings to other movies. For this each user is represented as a vector with a certain number of dimensions and a couple of distance metrics have been employed to find the distances between users. Once we have a set of similar users, a rating can be predicted based on the ratings of similar users for that particular movie.

Data set used : 100K dataset at http://grouplens.org/datasets/movielens/

The method is evaluated using a MAD value. The MAD achieved is about 0.8. Still huge scope for improvement.

Python, numPy, sciPy, pycharm IDE.
