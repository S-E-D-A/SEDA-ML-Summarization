# BIG DATA TEST



import numpy as np
import pickle


A1 = np.load('../../data/A1_matrix.npy')
A2 = np.load('../../data/A2_matrix.npy')
A3 = np.load('../../data/A3_matrix.npy')

vocabulary = np.load('../../data/vocabulary_list.npy')
fD_dictionary = pickle.load(open('../fD_pickled', "rb"))


fD_list = []
for item in vocabulary:
    fD_list.append(fD_dictionary[item])

fD = np.array(fD_list).reshape(1, len(fD_list))
fD = fD[0]

#print "Building fD map..."
#fD_map = np.memmap('fD_map.dat', dtype='float64', mode='w+', shape=(len(fD), len(fD)))

print "Building A map..."
A_mat = np.dot(np.dot(A1, A2), A3)
A_map = np.memmap('A_map.dat', dtype='float64', mode='w+', shape=A_mat.shape)


print "filling maps with data..."
#print fD
#for x in range(0,len(fD)):
#    print str(x)
#    fD_map[:,x] = fD[:]


A_map[:] = A_mat[:]

print "building output map"
prodmap = np.memmap('prodmap.dat', dtype='float64', mode='w+', shape=A_mat.shape)


print "fD Shape: " + str(np.transpose(fD).shape)
print "A_map: " + str(A_map[:,1])
print "A_map shape: " + str(A_map[:,1].shape)
for y in range(0, 10):
    for x in range(0, len(fD)):
        prodmap[x,y] = np.dot(np.transpose([fD[x]] * len(fD)), A_map[:,y])
    print y	
print "size of prodmap: " + str(prodmap.shape)










