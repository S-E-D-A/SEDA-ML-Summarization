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

from summ_generation import SummaryGeneration


vocabulary = {'cat', 'dog', 'mouse', 'fox'}
fD = numpy.random.rand(1,4)
A_one = numpy.random.rand(4,4)
A_two = numpy.random.rand(4,4)
A_three = numpy.random.rand(4,4)


c = SummaryGeneration(vocabulary, 4, 3, 200)
c.buildAFMatrix(fD, A_one, A_two, A_three)
