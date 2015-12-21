import math

arr1 = [71,73,75,80,80,80,78,76,75,73,71,71,71,73,75,76,76,68,76,76,75,73,71,70,70,69,68,68,72,74,78,79,80,80,78]
<<<<<<< HEAD
arr2 = [69,69,73,75,79,80,79,78,76,73,72,71,70,70,69,69,69,71,73,75,76,76,76,76,76,75,73,71,70,70,71,73,75,80,80]


class DTW():
	def __init__(self):
		#self.arr1 = arr1
		#self.arr2 = arr2
		self.DTW = []
	
	def dist(self, a, b):
		return math.sqrt((a-b)*(a-b))
	
	def new_arr(self, len1, len2):
		arr = []
		for i in range(len1):
			new_row = []
			for j in range(len2):
				new_row.append(0)
			arr.append(new_row)
		return arr
	
	def calc_DTW(self, a1, a2):
		self.DTW = self.new_arr(len(a1), len(a2))
	
		for i in range(len(a1)):
			self.DTW[i][0] = float("inf")
		for i in range(len(a2)):
			self.DTW[0][i] = float("inf")
	
		for i in range(len(a1)):
			for j in range(len(a2)):
				cost = self.dist(a1[i], a2[j])
				'''only traceback for 1 step !????????'''
				self.DTW[i][j] = cost + min(self.DTW[i][j-1], self.DTW[i-1][j], self.DTW[i-1][j-1])#min(DTW[i-1][j],DTW[i][j-1],DTW[i-1][j-1])
		#print DTW 
		return self.DTW[len(a1)-1][len(a2)-1]


dist = DTW() 
print "DIST",dist.calc_DTW(arr1, arr2)
=======
arr2 = [69,69,73,75,79,80,79,78,76,73,72,71,70,70,69,69,69,71,73,75,76,76,76,76,76,75,73,71,70,70,71,73,75,80,80,80,78]
INF = 10000000

def dist(a, b):
	return math.sqrt((a-b)*(a-b))

def new_arr(len1, len2):
	arr = []
	for i in range(len1):
		new_row = []
		for j in range(len2):
			new_row.append(0)
		arr.append(new_row)
	return arr

def DTW(a1, a2):

	DTW = new_arr(len(a1), len(a2))

	for i in range(len(a1)):
		DTW[i][0] = INF
	for i in range(len(a2)):
		DTW[0][i] = INF

	for i in range(len(a1)):
		for j in range(len(a2)):
			cost = dist(a1[i], a2[j])
			DTW[i][j] = cost + min(DTW[i][j-1],DTW[i-1][j],DTW[i-1][j-1])#min(DTW[i-1][j],DTW[i][j-1],DTW[i-1][j-1])

	print DTW 
	return DTW[len(a1)-1][len(a2)-1]


dist = DTW(arr1, arr2)
print "DIST",dist
>>>>>>> bb790598475ddad5257e4199c25bd9b296ad1e26
