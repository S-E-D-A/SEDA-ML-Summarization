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
		
		
