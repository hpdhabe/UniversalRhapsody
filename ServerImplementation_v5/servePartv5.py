from model import createModel
import os
import numpy as np
from subprocess import Popen, PIPE, STDOUT
from PIL import Image

from imageFilesTools import getImageData
from audioFilesTools import isMono
from config import batchSize
from config import filesPerGenre
from config import nbEpoch
from config import validationRatio, testRatio
from config import sliceSize
from config import slicesPath
from config import preTemp
from config import pixelPerSecond
import socket
import sys

import numpy as np
# from jsonsocket import Server
import pickle
from _thread import *
import threading

port = 55555
host = 'localhost'
nbClasses = 13
trainNb = 0

print_lock = threading.Lock()
model = createModel(nbClasses, sliceSize)
print ("Model Created...")
model.load('musicDNN.tflearn')



def threaded(c):
	try:
		data = b""
		# Recieve Array from client
		while True:
			print("Concatinating....")
			packet = c.recv(9999999999)
			if not packet:
				print_lock.release()
				break
			data += packet
		feed_data = pickle.loads(data)
		print ("Array Recieved...")
		NbSlices = len(feed_data)
		print ("Number of slices:   ", NbSlices)

		# Predict and assert results
		print ("Predicting...")
		results = model.predict(feed_data)
		np.set_printoptions(suppress=True)
		np.set_printoptions(precision=4)
		np.set_printoptions(threshold=np.inf)

		# Convert Results into usable data
		genre_data_temp = []
		for i in range (0, NbSlices):
			curr_max = results[i].max()
			genre_data_temp += np.where(results[i] == curr_max)
		genre_data = np.asarray(genre_data_temp)
		out_data = []
		for i in range (0, NbSlices):
			x =  i / NbSlices
			y =  genre_data[i][0]
			out_data.append([x,y]) 

		# Write results onto a file to send to client
		print ("Writing results...")
		with open("file2send", "wb") as file2send:
			pickle.dump(out_data, file2send)
		file2send.close()

		# Send File to client
		f = open ("file2send", "rb")
		l = f.read(1024)
		while(l):
			print("Sending...")
			c.send(l)
			l = f.read(1024)
		f.close()
		c.shutdown(socket.SHUT_WR)
		print("Send!!! ✅")


		print("End Of CurRent Thread!!!")

	except Exception as e:
		print (e)
		raise
		return
		



def Main():
	s = socket.socket()
	print ("socket created... ✅")
	s.bind (('',port))
	print ("socket binded to", port, "  ✅")
	s.listen(5)
	while True:
		c, addr = s.accept()
		print ("Got connection from ", addr, "	✅")
		print_lock.acquire()
		start_new_thread(threaded, (c,))
	s.close()


if __name__ == "__main__":
	Main()

