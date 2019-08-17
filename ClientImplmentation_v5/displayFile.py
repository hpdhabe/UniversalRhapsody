import pickle
import os


pickle_in = open("received","rb")
genre_dict = pickle.load(pickle_in)
print (genre_dict)