# TITLE:
#     Build Vocabulary
#
# DESCRIPTION:
#    Builds a vocabulary given path to word list of document set
#    Then stores the vocabulary as a pickled file that can be read in later during summary generation
#
# EXAMPLE:
#    python build_vocabulary.py <path-to-file>
#


import sys
import os
import string
import pickle
import ast


# test inputs
try:
    if len(sys.argv) != 2:
        print "Not enough input arguments. Please include the file you wish to parse in the command line."
        exit()
except:
    print "Trouble reading in input arguments. Please include first the file to read, then the name of the file for exporting"
    exit()


# retrieve SOLR document with all words in documents (vocabulary)
# OPEN FILESTREAM
#argv[1] = input file
try:
    infile = open(sys.argv[1],'r')
except:
    print "Trouble reading input file. Try again."
    exit()


# READ SENTENCES
doc = infile.read()
new_dict = ast.literal_eval(doc)

# PARSE INFILE
vocabulary = []

terms_list = new_dict['terms']['features']
vocabulary = [x for x in terms_list if not isinstance(x, int)]

# PICKLE AND EXPORT
#    Titled: vocabulary_pickled
with open('vocabulary_pickled', 'wb') as f:
    pickle.dump(vocabulary, f)






