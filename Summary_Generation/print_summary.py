# PRINT SUMMARY

import pickle
try:
	summary = pickle.load(open("best_summary", "rb"))

	print "\n\n SUMMARY GENERATED: \n\n"
	for i in range (0, len(summary)):
        	best_sentence = summary[i]
		sentence_string = ""
		for item in best_sentence:
			sentence_string = sentence_string + item
			sentence_string = sentence_string + " "
        	print sentence_string      
		print "\n"
except:
	print "No Summary has been generated. Nothing to print!"





