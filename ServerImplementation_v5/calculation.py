import numpy as np
import pickle

fname = "file2send"
NbSlices = 142

with open(fname, 'rb') as f:
    my_list = pickle.load(f)

data = np.asarray(my_list)    
np.set_printoptions(suppress=True)
np.set_printoptions(precision=8)
np.set_printoptions(threshold=np.inf)


# genre_data_temp = []
# for i in range (0, NbSlices):
# 	curr_max = data[i].max()
# 	genre_data_temp += np.where(data[i] == curr_max)

# genre_data = np.asarray(genre_data_temp)


# out_data = []

# for i in range (0, NbSlices):
# 	x =  i / NbSlices
# 	y =  genre_data[i][0]
# 	out_data.append([x,y]) 

print ("#######################################")
print (data)

