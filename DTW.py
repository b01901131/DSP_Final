import math
import numpy as np

arr1 = [71,73,75,80,80,80,78,76,75,73,71,71,71,73,75,76,76,68,76,76,75,73,71,70,70,69,68,68,72,74,78,79,80,80,78]
arr2 = [69,69,73,75,79,80,79,78,76,73,72,71,70,70,69,69,69,71,73,75,76,76,76,76,76,75,73,71,70,70,71,73,75,80,80]


class DTW():
	def __init__(self):
		#self.arr1 = arr1
		#self.arr2 = arr2
		self.DTW = []
	
	def dist(self, a, b):
		return np.linalg.norm(np.array(a)-np.array(b))
	
	#def new_arr(self, len1, len2):
	#	arr = np.zeros((len1, len2))
	#	return arr
	
	def calc_DTW(self, a1, a2):
		print "start"
		l1 = len(a1)
		l2 = len(a2)
		self.DTW = np.zeros((l1, l2))
		
		inf = np.full(l1, np.inf)
		self.DTW[:,0] = inf

		inf = np.full(l2, np.inf)
		self.DTW[0,:] = inf

		for i in range(l1):
			for j in range(l2):
				cost = self.dist(a1[i], a2[j])
				self.DTW[i][j] = cost + min(self.DTW[i][j-1], self.DTW[i-1][j], self.DTW[i-1][j-1])#min(DTW[i-1][j],DTW[i][j-1],DTW[i-1][j-1])
		#print DTW 
		print "finish"
		return self.DTW[l1-1][l2-1]


#dist = DTW() 
#print "DIST",dist.calc_DTW(arr1, arr2)