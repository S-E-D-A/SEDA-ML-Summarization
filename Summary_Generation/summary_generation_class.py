# Title:
#	Summary Generation
#
# Source:
#	Query-Oriented Multi-Document Summarization via Unsupervised Deep Learning
#	Yan Liu, Sheng-hua Zhong, Wenjie Li
#	Department of Computing, The Hong Kong Polytechnic University
#	AAAI, 2012
#
# Description: 
#	This class is the final component to Liu's summarization system.
#	It builds an importance matrix (AF) from values fed from a 
#	deep neural network.  It then extracts 10 word with largest
#	AF value i every nth node and uses these to calculate the
#	importance of every sentence in the document. Dynamic
#	programming is then used to solve the optimization problem
#	of determining which sentences should be placed in the summary.
#
#
#

import cPickle
import gzip
import os
import sys
import time
import copy

import numpy
from numpy import dot

import pickle

# import theano
# import theano.tensor as T
# from theano.tensor.shared_randomstreams import RandomStreams



class SummaryGeneration(object):

	def __init__(self, vocabulary, numNodes, lambd, N_s):
		"""
		:desc: Summary Generation Constructor
	
		:param vocabulary: list of words in vocabulary
	
		:param numNodes: number of nodes in H3
	
		:param lambd: query word importance factor
	
		:param N_s: max size of summary
		"""

		self.vocabulary = vocabulary
		self.i = len(vocabulary)
		self.n = numNodes
		self.lambd = lambd
		self.N_s = N_s

	
	def buildAFMatrix(self, fD, A_one, A_two, A_three):
		"""
		:desc: Summary Generation AF Matrix Generator

		:param fD: feature vector (tf score) across entire document set

		:param A_one: pairwise connections in first layer

		:param A_two: pairwise connections in second layer

		:param A_three: pairwise connections in third layer
		"""
		
		assert (self.i,) == fD.shape

		self.A_one = A_one
		self.A_two = A_two
		self.A_three = A_three
		self.A_mat = dot(dot(A_one, A_two), A_three)	

		try:
			print "Retrieving A Map..."
			self.A_map = numpy.memmap('A_map.dat', dtype='float64', mode='r', shape=self.A_mat.shape)
			print "Retrieving AF Map..."
			self.AF = numpy.memmap('prodmap.dat', dtype='float64', mode='r', shape=self.A_mat.shape)
		except:
			print "No AF Matrix Found. Creating memory maps..."
			self.A_map = numpy.memmap('A_map.dat', dtype='float64', mode='w+', shape=self.A_mat.shape)
			self.AF = numpy.memmap('prodmap.dat', dtype='float64', mode='w+', shape=self.A_mat.shape)
			for y in range(0, 10):
    				for x in range(0, len(fD)):
        				self.AF[x,y] = dot(numpy.transpose([fD[x]] * len(fD)), self.A_map[:,y])
    				print y

		self.AF = numpy.transpose(self.AF)

	def wordExtraction(self):
		"""
		:desc: Word Extraction from AF Matrix
	
		"""

		assert self.i >= 10

		self.indicesMatrix = numpy.zeros(shape=(10, self.n))
		self.UN = []

		dummy = copy.deepcopy(self.AF)
		for x in range (0, 10):
			indices = dummy.argmax(axis=0)
			self.indicesMatrix[x,:] = indices
			dummy[indices,range(0,self.n)] = -1000	

		for x in range(0,10):
			cur_list = []
			for y in range(0,self.n):
				item = self.vocabulary[self.indicesMatrix[x,y].astype(int)]
				cur_list.append(item)

			self.UN.append(cur_list)



	def sentenceImportance(self, sentences, query):
		"""
		:desc: Sentence Importance Calculation

		:param sentences: list of sentences from document
			the list is a list of sentences
			each sentence is a list of words

		:param query: list of words from query
		"""

		self.sentences = sentences
		self.query = query
		self.t = len(sentences)
		self.rolloutUN = [item for sublist in self.UN for item in sublist]

		self.sentenceImportanceVector = numpy.zeros(shape=(1,self.t))
		self.sentenceLengthVector = numpy.zeros(shape=(1,self.t))
		self.sentenceIndexVector = numpy.zeros(shape=(1,self.t))

		print "num sentences: " + str(self.t)

		print "locating sentence information data..."
		try:
			self.sentenceInformation = pickle.load(open("sentenceInformation", "rb"))
			self.sentenceIndexVector = self.sentenceInformation[0]
			self.sentenceImportanceVector = self.sentenceInformation[1]
			self.sentenceLengthVector = self.sentenceInformation[2]
		except:
			print "file not found. regenerating..."
			for x in range(0,self.t):
				cur_sentence = self.sentences[x]
				numWords = len(cur_sentence)

				self.sentenceLengthVector[0,x] = numWords

				score = 0

				for i in range(0, numWords):
					cur_word = cur_sentence[i]
				
					w = 0
				
					if (cur_word in self.rolloutUN and cur_word in query):
						w = self.lambd
					elif (cur_word in self.rolloutUN):
						w = 1
				
					score = score + w

				self.sentenceImportanceVector[0,x] = score	
				self.sentenceIndexVector[0,x] = x
		
				print "Evaluated Sentence: " + str(x)

			self.sentenceInformation = [self.sentenceIndexVector, self.sentenceImportanceVector, self.sentenceLengthVector]			
			print "writing sentence information to file..."
			pickle.dump(self.sentenceInformation, open("sentenceInformation", "wb"))	


	def optimizeSummary(self):
		"""
		:desc: Summary Optimization using Dynamic Programming
		"""
		
		lambd_in = 0
		score = 0
		cur_summ = []
		remaining_sentences = copy.deepcopy(self.sentenceInformation)
		scores = [] #2D list containing vectors of scores of summary lists
		solutions = [] #2D list containing vectors of indices of sentences in summary

		print "finding summary recursively..."		

		self.findSummaryDP()
		
		self.best_summary_indices = []
		K = int(self.N_s) - 1

		for i in range (len(self.sentenceIndexVector[0]) - 1, 0, -1):
			if self.keep[i][K] == 1:
				self.best_summary_indices.append(i)
				K = K - self.sentenceLengthVector[0][i]
		
		self.best_summary_score = self.m_matrix
		self.best_summary = []

		for x in range(0,len(self.best_summary_indices)):
                        cur_index = self.best_summary_indices[x]
                        self.best_summary.append(self.sentences[cur_index])



		"""
		self.findSummary(lambd_in, score, cur_summ, remaining_sentences, solutions, scores, self.N_s)


		self.potential_summaries_indices = copy.deepcopy(solutions)
		self.potential_summaries_scores = copy.deepcopy(scores)

		index = numpy.argmax(self.potential_summaries_scores)

		self.best_summary_indices = self.potential_summaries_indices[index]
		self.best_summary_score = self.potential_summaries_scores[index]
		
		self.best_summary = []


		for x in range(0,len(self.best_summary_indices)):
			cur_index = self.best_summary_indices[x]
			self.best_summary.append(self.sentences[cur_index.astype(int)])
		"""	

	def findSummaryDP(self):
		"""
		:desc: dynamic programming solution for solving optimization problem
		returns matrix of scores and word counts. find max for answer
		"""
        
		# initialize m_matrix
		matrix_shape = (int(len(self.sentenceImportanceVector[0])), int(self.N_s))

		self.m_matrix = numpy.zeros(matrix_shape)
		self.keep = numpy.zeros(matrix_shape)	    

		# run dP
		for i in range (1,len(self.sentenceIndexVector[0])):
			for j in range(0,int(self.N_s)):
				if j >= self.sentenceLengthVector[0][i]:
					self.m_matrix[i][j] = max(self.m_matrix[i-1][j], self.m_matrix[i-1][j-self.sentenceLengthVector[0][i]] + self.sentenceImportanceVector[0][i])
					self.keep[i][j] = 1
				else:
					self.m_matrix[i][j] = self.m_matrix[i-1][j] 




    	def findSummary(self, lambd_in, score, cur_summ, remaining_sentences, solutions, scores, N_s):
		"""
		:desc: recursive function for solving the optimization problem
			returns the collection of summary possibilities in solutions list

		:param lambd_in: current number of words

		:param score: current score list corresponding to current summary

		:param cur_summ: current summary list of indices of sentences

		:param remaining_sentences: sentences list that could be added to current summary

		:param solutions: solutions list containing all possible summaries

		:param scores: scores list corresponding to solutions list

		:param N_s: max number of words in a summary
		"""

		if (lambd_in > N_s):
			return	

		if (len(remaining_sentences[0][0]) == 0):
			solutions.append(cur_summ)
			scores.append(score)

		for x in range(0, len(remaining_sentences[0][0])):

			if (remaining_sentences[0][0][x] not in cur_summ):
				lambd_new = copy.deepcopy(lambd_in) + remaining_sentences[2][0][x]
				score_new = copy.deepcopy(score) + remaining_sentences[1][0][x]
				cur_summ_new = copy.deepcopy(cur_summ)
				cur_summ_new.append(remaining_sentences[0][0][x])
				a = numpy.delete(remaining_sentences[0][0], x)
				b = numpy.delete(remaining_sentences[1][0], x)
				c = numpy.delete(remaining_sentences[2][0], x)
				rs_new = [[a],[b],[c]]
				self.findSummary(lambd_new, score_new, cur_summ_new, rs_new, solutions, scores, N_s)
			else:
				lambd_new = copy.deepcopy(lambd_in)
				score_new = copy.deepcopy(score)
				a = numpy.delete(remaining_sentences[0][0], x)
				b = numpy.delete(remaining_sentences[1][0], x)
				c = numpy.delete(remaining_sentences[2][0], x)
				rs_new = [[a], [b], [c]]
				cur_summ_new = copy.deepcopy(cur_summ)
				self.findSummary(lambd_new, score_new, cur_summ_new, rs_new, solutions, scores, N_s)

		if (lambd_in <= N_s):
			if (cur_summ not in solutions):
				solutions.append(cur_summ)
				scores.append(score)
		
		print "length of remaining sentences: " + str(len(remaining_sentences[0][0]))
		return






