#!/usr/bin/python
# -*- coding: utf8 -*-
import math
import numpy as np
import cPickle as pickle
import scipy.cluster.hierarchy as hac
from scipy.cluster.vq import *

arr1 = [71,73,75,80,80,80,78,76,75,73,71,71,71,73,75,76,76,68,76,76,75,73,71,70,70,69,68,68,72,74,78,79,80,80,78]
arr2 = [69,69,73,75,79,80,79,78,76,73,72,71,70,70,69,69,69,71,73,75,76,76,76,76,76,75,73,71,70,70,71,73,75,80,80]
arr3 = pickle.load(open("吳建昇小雞雞_mfcc_13.pkl", "rb"))

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
	
	def calc_DTW(self, a1, a2, _hac):
		#print "start"
		if _hac:
			a1 = self.calc_HAC(a1)
			a2 = self.calc_HAC(a2)
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
		#print "finish"
		return self.DTW[l1-1][l2-1]

	def calc_HAC(self, a):
		h = hac.linkage(a, method='complete')
		h = hac.fcluster(h, 15, 'maxclust')
		h = np.asarray(h)
		index = h.argsort()
		a_sort = a[index]
		num_cnt = np.zeros(15)
		for i in range(1,16):
			num_cnt[i-1] = list(h).count(i)
		prev_index = 0
		hac_a = np.zeros((15,13))
		for i in range(len(num_cnt)):
			for j in range(int(num_cnt[:i].sum()), int(num_cnt[:i+1].sum())):
				hac_a[i][:] += a[j] / num_cnt[i]
		return hac_a

	def calc_Kmean(self, a):
		kmean_a = kmeans2(a, 15)
		return kmean_a

dist = DTW() 
print "DIST",dist.calc_Kmean(arr3)