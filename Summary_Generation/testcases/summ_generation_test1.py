# Title:
#	Summary Generation - Test
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
from numpy import dot

#import theano
#import theano.tensor as T
#from theano.tensor.shared_randomstreams import RandomStreams

sys.path.append('/Users/hobeykuhn/Documents/Schoolwork/University of Michigan/MSAIL/SEDA-ML-Summarization');

from summary_generation_class import SummaryGeneration


vocabulary = ['cat', 'dog', 'mouse', 'fox', 'bear', 'tiger', 'ram', 'person', 'gen', 'f', 'd', 's', 'a', 'r', 'y']
sentences = [['the','cat','jumped','over','the','moon'],['the','dog','fox','f','r'], ['gen', 'd', 's', 'mouse', 'something']]
query= ['dog', 'f', 'r']
fD = numpy.random.rand(1,15)
A_one = numpy.random.rand(15,15)
A_two = numpy.random.rand(15,15)
A_three = numpy.random.rand(15,15)


c = SummaryGeneration(vocabulary, 15, 3, 16)
c.buildAFMatrix(fD, A_one, A_two, A_three)
print 'AF MATRIX'
print c.AF

c.wordExtraction()
#print c.indicesMatrix
#print c.UN

c.sentenceImportance(sentences, query)
print 'SENTENCE INFORMATION'
print c.sentenceInformation

c.optimizeSummary()
print 'POTENTIAL SUMMARIES'
print c.potential_summaries_indices
print c.potential_summaries_scores
print 'BEST SUMMARY'
print c.best_summary_indices
print c.best_summary_score
print c.best_summary
