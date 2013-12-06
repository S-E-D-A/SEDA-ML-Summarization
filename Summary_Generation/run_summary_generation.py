# TITLE
#    Run Summary Generation
#
# DESCRIPTION
#    Given paths for vocabulary, query, and A matrices, this python script will build a summary generation class instance
#    It will then generate a summary with these inputs
#
#
#
# EXAMPLE
#    python run_summary_generation.py vocabulary_pickled fD_pickled <name_of_input_sentences_document> <name_of_input_query_document>



import pickle
import gzip
import os
import sys
import time

import numpy
from numpy import dot


# test inputs
try:
    if len(sys.argv) != 5:
        print "Not enough input arguments. Please include the file you wish to parse in the command line."
        exit()
except:
    print "Trouble reading in input arguments. Please include first the file to read, then the name of the file for exporting"
    exit()

# OPEN FILES
#argv[1] = vocabulary_pickled
#....
#
print "loading inputs..."
try:
    vocabulary = pickle.load(open(sys.argv[1], "rb"))
    fD = pickle.load(open(sys.argv[2], "rb"))
    sentences = pickle.load(open(sys.argv[3], "rb"))
except:
    print "Trouble reading input file. Try again."
    exit()
try:
    query = pickle.load(open(sys.argv[4], "rb"))
except:
    print "No query exists... Setting to empty list"
    query = []


print "retrieving weight matrices..."
A1 = numpy.load('../data/A_matrices/A1_matrix.npy')
A2 = numpy.load('../data/A_matrices/A2_matrix.npy')
A3 = numpy.load('../data/A_matrices/A3_matrix.npy')

print "length of A1: " + str(len(A1))
print "length of A2: " + str(len(A2))
print "length of A3: " + str(len(A3))
print "length of fD: " + str(len(fD))








