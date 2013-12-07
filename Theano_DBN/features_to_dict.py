import theano
import numpy
import random

from clean_doc import *

#Converts the list passed into it into dictionary format,
#in the form specified below, to be used to extract
#features cleanly
def to_dict(l):
    if not isinstance(l[1], list):
        return dict(zip(*[iter(l)]*2))
    rv = zip(*[iter(l)]*2)
    for k, v in rv:
        return {k: to_dict(v)}
	


#Returns a dictionary version of the feature table, and a key-table
#containing the name of each document of the corresponding index in the 
#feature list
#dwf[i][docnames_table[i]]['features'] = 
# list of words + values, where every even index j (inc. 0) is
# a word in the document, and the odd numbered index j+1 is a
# list ['tf', val, 'df', val, 'tf-idf', val]
#dt[word_ind] = 'word' 
#full_dict_features[doc_name][word_ind]['word']['tf-idf']
# = the corresponding word's tf-idf value
def to_full_feature_list(doc_name, ndocs):
	
	
	doc_string = open(doc_name).read()
	doc_string = clean_doc(doc_string)
	
	feature_list = eval('[{0}]'.format(doc_string))
	dwf = []
	dt = {}

	full_dict_features = {}
	
	for i in xrange(ndocs):
	    index = i*2
            dwf.append(to_dict([feature_list[index], feature_list[index + 1]]))
	    dt[i] = feature_list[index]
	    for j in xrange(len(dwf[i][dt[i]]['features'])/2):
		feature_index = j*2
		try:    	
			full_dict_features[feature_list[index]].append(to_dict([ dwf[i][dt[i]]['features'][feature_index] , dwf[i][dt[i]]['features'][feature_index + 1] ]))
		except:
			full_dict_features[feature_list[index]] = [to_dict([ dwf[i][dt[i]]['features'][feature_index] , dwf[i][dt[i]]['features'][feature_index + 1] ])]	
	return dwf, dt, full_dict_features

#Extracts the feature lists given the document name and 
#specified number of documents, then constructs a 
#feature array, where each row represents one example,
#and each column represents a feature
#Returns an (ndocs x number of features) array, 
def construct_dataset(doc_name, ndocs):
	dwf, dt, fdf = to_full_feature_list(doc_name, ndocs)
	all_words_dict = {}
	word_ind_dict = {}
	ind_counter = 0;
	total_vocabulary = []
	#Change this to fit the type of value you want to extract
	#i.e. 'tf', 'df', or 'tf-idf'
	freq_type = 'tf-idf'	

	for docname in fdf:
	    for word_ind in xrange(len(fdf[docname])):
		for word_str in fdf[docname][word_ind]:
		    if word_str in word_ind_dict:
		        all_words_dict[word_str] = 0
		    else:
		        all_words_dict[word_str] = 0		    
			word_ind_dict[word_str] = ind_counter
			total_vocabulary.append(word_str)
			ind_counter = ind_counter + 1
			
	

	print "total # of words/features = ...", len(all_words_dict)
	#print all_words_dict
	
	vocab_filename = '../data/vocabulary_list'
	numpy.save(vocab_filename, total_vocabulary)
	print "...saved vocabulary list to ", vocab_filename,".npy"
		
	#Create blank training set matrix, size=(ndocs x |D|)
	data_set = [];	
	for i in xrange(ndocs):
	    data_set.append([])
	    for j in xrange(len(all_words_dict)):
	    	data_set[i].append(0)

	doc_ind = 0;

	for docname in fdf:
	    for word_ind in xrange(len(fdf[docname])):
		for word_str in fdf[docname][word_ind]:
		   val = fdf[docname][word_ind][word_str][freq_type]
		   data_set[doc_ind][word_ind_dict[word_str]] = val
	    doc_ind = doc_ind + 1
	return data_set
	

#Splits the training data
def split_data(data_set, ndocs):
	
	#train_set = data_set[40:]
	#valid_set = data_set[0:20]
	#test_set = data_set[20:40]
        train_set = data_set[0:ndocs/2]
        valid_set = data_set[ndocs/2:ndocs/2 + ndocs/4]
        test_set = data_set[ndocs/2 + ndocs/4:]
	return train_set, valid_set, test_set

#Makes the data shared to work with theano DBN.py
def make_shared_data(data_subset, borrow = True):
	return theano.shared(numpy.asarray(data_subset,
						dtype=theano.config.floatX),
				borrow = borrow)

def load_data_australia(doc_name, ndocs):
	trs, vs, tes = split_data(construct_dataset(doc_name, ndocs), ndocs)
    	nfeats = len(trs[0])
       
	tr_x = make_shared_data(trs)
	val_x = make_shared_data(vs)
	tes_x = make_shared_data(tes)	

	#Add garbage y-values to appease theano
	tr_y_ = [0]*len(trs)
	val_y_ = [0]*len(vs)
	tes_y_ = [0]*len(tes)
		
	tr_y = theano.tensor.cast(make_shared_data(tr_y_), 'int32')
	val_y = theano.tensor.cast(make_shared_data(val_y_), 'int32')
	tes_y = theano.tensor.cast(make_shared_data(tes_y_), 'int32')

	print 'Training set size: ', len(trs)
        print 'Validation set size: ', len(vs)
        print 'Test set size: ', len(tes) 		
	rval = [(tr_x, tr_y),(val_x, val_y),(tes_x, tes_y)]
	return nfeats, rval
