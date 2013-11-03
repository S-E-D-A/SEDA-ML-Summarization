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

import numpy

import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams



class SummaryGeneration:

	def __init__(self, vocabulary, numNodes, lambd, N_s)
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

	self.AF = numpy.zeros(shape=(i,n)







)
