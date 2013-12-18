#!/usr/bin/env python

# In order for ROUGE to evaluate a dataset it requires each peer 
# and machine summary file name included as a task XML field in 
# the settings.xml file. 
def writeRougeSettingTask(file, file_name, directory):
    file.write('<EVAL ID="' + file_name + '">\n')
    file.write('<MODEL-ROOT>' + directory + '/models</MODEL-ROOT>\n')
    file.write('<PEER-ROOT>' + directory + '/systems</PEER-ROOT>\n')

    file.write('<INPUT-FORMAT TYPE="SEE">  </INPUT-FORMAT>\n')

    file.write('<PEERS>\n')
    file.write('<P ID="' + file_name + '">' + file_name + '.html</P>\n')
    file.write('</PEERS>\n')

    file.write('<MODELS>\n')
    file.write('<M ID="' + file_name + '">' +  file_name + '.html</M>\n')
    file.write('</MODELS>\n')
    file.write('</EVAL>\n\n')

# This function takes an XML file from the corpus
# and parses out the catchprases and stores them in ROUGE html format
def createRougeHTMLSummaryFromAustliiCatchphrases(filename, in_human_summaries_directory, out_model_directory):
    import sys
    import xml.etree.ElementTree as ET
    
    # Reads in the .xml file from which the catchphrases are extracted (summaries)
    infile = open(in_human_summaries_directory + '/' + filename.replace('_summary', '') + '.xml', 'r')
    doc = infile.read()
    
    # Find the beginning and end index of element <catchphrases> in xml and store them as a string
    start_index = doc.find('<catchphrases>')
    end_index = doc.find('</catchphrases>') + len('</catchphrases>')
    doc = doc[start_index:end_index]
    
    # Fix incorrect XML formatting in dataset
    doc = doc.replace('"id=', 'id="')
    
    # Parse XML as an object
    xmldoc = ET.fromstring(doc)
    
    f = open(out_model_directory + "/" + filename + '.html','w')
    f.write("<html>\n")
    f.write("<head><title>" + filename + "</title></head>\n")
    f.write('<body bgcolor="white">\n')
    
    i = 0;
    for child in xmldoc:
        f.write('<a name="' + str(i) + '">[' + str(i) + ']</a> <a href="#' + str(i) + '" id=' + str(i) +'>'+ child.text +'</a>\n')
        i+=1
    
    f.write("</body>\n")
    f.write("</html>")
        
    f.close()

# This generates the summary in Rouge html format given a file
def createRougeHTMLSummaryFromSEDASummaries(file, out_system_directory):
    import pickle
    try:
        # Get the name of the file
        file_name = os.path.basename(file)
        
        # Loads the pickled machine generate summary
        summary = pickle.load(open(file, "rb"))
        
        f = open(out_system_directory + "/" + file_name + '.html','w')
        f.write("<html>\n")
        f.write("<head><title>" + file_name + "</title></head>\n")
        f.write('<body bgcolor="white">\n')
        
        for i in range (0, len(summary)):
                best_sentence = summary[i]
                sentence_string = ""
                for item in best_sentence:
                        sentence_string = sentence_string + item
                        sentence_string = sentence_string + " "
                f.write('<a name="' + str(i) + '">[' + str(i) + ']</a> <a href="#' + str(i) + '" id=' + str(i) +'>'+ sentence_string +'</a>\n')
        
        f.write("</body>\n")
        f.write("</html>")
            
        f.close()
    except:
        print "No Summary has been generated. Nothing to print!"

def generateRougeEvaluationFiles(in_machine_summaries_directory, in_human_summaries_directory, out_directory):
    import subprocess
    import sys
    import glob
    import os
    # Append rougeFiles to the output directory
    out_directory+='/rougeFiles';
    
    # Where the Rouge prepared system generated summaries go
    out_system_directory = os.path.abspath(out_directory + "/systems");
    
    # Where the Rouge prepared human generated summaries go
    out_model_directory = os.path.abspath(out_directory + "/models")
    
    # Create directories to store Rouge prepared output if they
    # don't already exist
    if not os.path.exists(out_system_directory):
        os.makedirs(out_system_directory)
    if not os.path.exists(out_model_directory):
        os.makedirs(out_model_directory)
        
    # Root ROUGE settings.xml file
    rouge_settings_file = open(out_directory + '/settings.xml','w')
    rouge_settings_file.write('<ROUGE_EVAL version="1.55">\n\n')
    
    # Iterate through all files and create html summaries
    for file in glob.glob(in_machine_summaries_directory + "/*_summary"):
        file_name = os.path.basename(file)
        createRougeHTMLSummaryFromSEDASummaries(file, out_system_directory)
        createRougeHTMLSummaryFromAustliiCatchphrases( file_name, in_human_summaries_directory, out_model_directory )
       
        writeRougeSettingTask(rouge_settings_file, file_name, 
            out_directory)
        
    rouge_settings_file.write('</ROUGE_EVAL>\n')
    rouge_settings_file.close()


################################################
################# Main Script ##################
################################################

import os, sys

# Get the absolute path of this script
abspath = os.path.abspath(__file__)

# Remove the filename to obtain the directory path
dname = os.path.dirname(abspath)

# The root folder of SEDA-ML
SEDA_ML_root = os.path.abspath(dname + "/../../");

# Path to machine generated summaries
in_machine_summaries_directory = os.path.abspath(SEDA_ML_root + "/data/Generated_Summaries");

# Check if system generated summaries are present,
# if not, exit
if not os.path.isdir(in_machine_summaries_directory):
	print "### Error. ###";
	print in_machine_summaries_directory + " is not present.";
	print "Plese makes sure generated system summareis are in the above folder.";
	exit(1);

# Path to human generated summaries
in_human_summaries_directory = os.path.abspath(SEDA_ML_root + "/data/corpus/fulltext");

# Where to store the generated Rouge files
if len(sys.argv) > 1:
	out_directory = SEDA_ML_root + '/data/' + sys.argv[1];
else:
	out_directory = SEDA_ML_root + '/data/EvaluationOutput'

print "Generating Rouge files in " + out_directory

# Call the chain of commands to generate all Rouge files
generateRougeEvaluationFiles(in_machine_summaries_directory, in_human_summaries_directory, out_directory)
