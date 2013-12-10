# TITLE
#    Parse Document into Sentences
#
# DESCRIPTION
#    Given an input file (full path), parse xml sentences into numpy sentences
#    Store the numpy array in a file called document_senteces.npy
#    Numpy array should be an array of sentences of words
#
#    NOTE: Be sure that the solr_xml_files directory corresponds to the current document set!
#
# EXAMPLE
#    python parse_document_into_sentences.py path/to/file/06_001.xml


import sys
import os
import xml.etree.ElementTree as ET
import string
import pickle


# test inputs
try:
    if len(sys.argv) != 2:
        print "Not enough input arguments. Please include the file you wish to parse in the command line."
        exit()
except:
    print "Trouble reading in input arguments. Please include first the file to read, then the name of the file for exporting"
    exit()



# OPEN FILESTREAM
#argv[1] = input file
try:
    infile = open(sys.argv[1],'r')
except:
    print "Trouble reading input file. Try again."
    exit()

parser = ET.XMLParser()
parser.parser.UseForeignDTD(True)
parser.entity['eacute'] = 'e'
parser.entity['nbsp'] = ' '
parser.entity['tm'] = 'TM'
parser.entity['reg'] = 'R'
parser.entity['ccedil'] = 'c'
parser.entity['iuml'] = 'i'
parser.entity['agrave'] = 'A'
parser.entity['egrave'] = 'E'
parser.entity['aacute'] = 'A'
parser.entity['ecirc'] = 'E'
parser.entity['auml'] = 'A'
parser.entity['szlig'] = 'B'
parser.entity['ocirc'] = 'O'
parser.entity['ouml'] = 'O'
parser.entity['acirc'] = 'A'
parser.entity['ouml'] = 'O'
parser.entity['uuml'] = 'U'
parser.entity['Eacute'] = 'E'
parser.entity['igrave'] = 'I'
parser.entity['aelig'] = 'ae'
parser.entity['icirc'] = 'I'
parser.entity['euml'] = 'E'
parser.entity['oslash'] = 'O'
parser.entity['Aring'] = 'A'
parser.entity['yacute'] = 'y'
parser.entity['ntilde'] = 'n'
parser.entity['oslash'] = 'O'
parser.entity['Ouml'] = 'O'


# READ SENTENCES
doc = infile.read()
xmldoc = ET.fromstring(doc, parser=parser);

# PARSE INFILE
sentences = []
table = string.maketrans("","")

for sentence in xmldoc.iter('field'):
    if sentence.attrib == {'name': 'features'}:
	removed_punc_sentence = sentence.text.encode('utf8', 'ignore').translate(table, string.punctuation)
        words = removed_punc_sentence.split()
        sentences.append(words)

# EXPORT SENTENCE ARRAY TO FILE (pickle)
#    Titled: <inputfile>_sentences_array
fileName, fileExtension = os.path.splitext(os.path.basename(sys.argv[1]))
outfile = fileName + '_sentences_array'
with open(outfile, 'wb') as f:
    pickle.dump(sentences, f)


