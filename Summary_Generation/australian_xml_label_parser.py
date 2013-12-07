import sys
import xml.etree.ElementTree as ET


# test inputs
try:
    if len(sys.argv) != 3:
        print "Not enough input arguments. Please include first the file to read, then the name of the file for exporting"
        exit()
except:
    print "Trouble reading in input arguments. Please include first the file to read, then the name of the file for exporting"
    exit()


# OPEN FILESTREAM
#argv[1] = input file
#argv[2] = output file
try:
    #infile = ET.parse(sys.argv[1])
    infile = open(sys.argv[1],'r')
except:
    print "Trouble reading input file. Try again."
    exit()

#try:
#    outfile = open(sys.argv[2],'w')
#except:
#    print "Trouble creating output file. Try again."
#    exit()


# INIT OUTPUT DOCUMENT

# READ SENTENCES
doc = infile.read()
index = doc.find('<catchphrases>')
index_two = doc.find('</catchphrases>') + 15
doc = doc[index:index_two]

f = open(sys.argv[2], 'w')
f.write(doc)



# close output file
#outfile.close()