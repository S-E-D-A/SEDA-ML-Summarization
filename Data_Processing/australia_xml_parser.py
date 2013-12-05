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
index = doc.find('<sentences>')
index_two = doc.find('</sentences>') + 12
doc = doc[index:index_two]

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
xmldoc = ET.fromstring(doc, parser=parser)

# WRITE XML
new_doc = ET.Element('add')
doc_tag = ET.SubElement(new_doc, 'doc')
ET.SubElement(doc_tag, 'field', attrib={"name": "id"}).text = sys.argv[1]

for sentence in xmldoc.findall('sentence'):
    ET.SubElement(doc_tag, 'field', attrib={"name": "features"}).text = sentence.text

tree = ET.ElementTree(element=new_doc)
tree.write(sys.argv[2])




# close output file
#outfile.close()
