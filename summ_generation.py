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

		self.AF = numpy.zeros(shape=(self.i,self.n))

	
	def buildAFMatrix(self, fD, A_one, A_two, A_three):
		"""
		:desc: Summary Generation AF Matrix Generator

		:param fD: feature vector (tf score) across entire document set

		:param A_one: pairwise connections in first layer

		:param A_two: pairwise connections in second layer

		:param A_three: pairwise connections in third layer
		"""
				
		assert (1, self.i) == fD.shape

		self.F = numpy.transpose(numpy.tile(fD, [self.n, 1]))
		self.A_one = A_one
		self.A_two = A_two
		self.A_three = A_three
	
		self.AF = dot(dot(dot(self.F, A_one), A_two), A_three)


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

		self.sentenceInformation = [[self.sentenceImportanceVector], [self.sentenceLengthVector]]			
		


	def optimizeSummary(self):
		"""
		:desc: Summary Optimization using Dynamic Programming
		"""
		
		lambd_in = 0
		score = []
		cur_summ = []
		remaining_sentences = copy.deepcopy(self.sentenceInformation)
		scores = [] #2D list containing vectors of scores of summary lists
		solutions = [] #2D list containing vectors of indices of sentences in summary


		findSummary(lambd_in, score, cur_summ, remaining_sentences, solutions, scores, self.N_s)


	def findSummary(lambd_in, score, cur_summ, remaining_sentences, solutions, scores, N_s):
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
			cur_summ.pop()
			score.pop()

			if (cur_summ not in solutions):
				solutions.append(cur_summ)
				scores.append(sum(score))
			return
		
		for x in range(0, len(remaining_sentences))
			lambd_new = lambd_in + remaining_sentences[1][0][x]
			score_new = score.append(remaining_sentences[0][0][x])
			cur_summ.append(x)
			a = numpy.delete(remaining_sentences[0][0][x])
			b = numpy.delete(remaining_sentences[1][0][x])
			rs_new = [a,b]
			findSummary(lambd_new, score_new, cur_summ, rs_new, solutions, scores, N_s)

		return






