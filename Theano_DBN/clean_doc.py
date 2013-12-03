from string import *
def clean_doc(doc_string):
	uniqueKey_ind = doc_string.find("'uniqueKey'")
	squareBracket_ind = doc_string.rfind(']',0,uniqueKey_ind)
	firstFileNameQuote_ind = doc_string.find("'",squareBracket_ind,uniqueKey_ind)
	return doc_string[firstFileNameQuote_ind:len(doc_string) - 3]
