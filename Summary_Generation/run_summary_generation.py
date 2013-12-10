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
#    python run_summary_generation.py ../data/vocabulary_list.npy fD_pickled <name_of_input_sentences_document> <name_of_input_query_document> <lambda> <summ_size>



import pickle
import gzip
import os
import sys
import time

import numpy
from numpy import dot

from summary_generation_class import SummaryGeneration


# test inputs
try:
    if len(sys.argv) != 7:
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
    vocabulary = numpy.load(sys.argv[1])
    fD_dictionary = pickle.load(open(sys.argv[2], "rb"))
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
A1 = numpy.load('../data/A1_matrix.npy')
A2 = numpy.load('../data/A2_matrix.npy')
A3 = numpy.load('../data/A3_matrix.npy')

lambd = sys.argv[5]
num_S = sys.argv[6]


# Create fD array with dictionary
fD_list = []
for item in vocabulary:
    fD_list.append(fD_dictionary[item])

fD = numpy.array(fD_list).reshape(1, len(fD_list))
fD = fD[0]

print "printing dimensions of input..."
print "A1 Matrix: " + str(A1.shape)
print "A2 Matrix: " + str(A2.shape)
print "A3 Matrix: " + str(A3.shape)
print "vocabulary: " + str(len(vocabulary))
print "fD: " + str(fD.shape)

# Build Summary Generation
print "Building summary generation..."
c = SummaryGeneration(vocabulary, len(A1), lambd, num_S)
print "Building AF Matrix..."
c.buildAFMatrix(fD, A1, A2, A3)
print 'AF MATRIX'
print c.AF

# Extract Words
print "Word Extraction..."
c.wordExtraction()

# Sentence Importance
print "Generating sentence importance..."
c.sentenceImportance(sentences, query)

#Optimizing Summary
print "Optimizing Summary..."
c.optimizeSummary()

#Dump Product
print "Dumping optimized summary into pickle file"
pickle.dump(c.best_summary_indices, open("best_summary_indices", "wb"))
pickle.dump(c.best_summary_score, open("best_summary_score", "wb"))
pickle.dump(c.best_summary, open("best_summary", "wb"))






