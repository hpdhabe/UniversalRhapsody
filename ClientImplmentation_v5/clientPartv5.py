import socket
import pickle
import numpy as np
import sys
import os
import time
import numpy as np
import json, codecs
from subprocess import Popen, PIPE, STDOUT
from PIL import Image
# from jsonsocket import Client

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
from eq_changer_v5 import changer
from _thread import *
import threading

print ("Starting Client...")
currentPath = os.path.dirname(os.path.realpath(__file__)) 
file = "test.mp3"
newFilename = "testmono"


def Start_Playback():
	try:
		changer(file)
		
	except Exception as e:
		print(e)
		raise
		return

def Send_File_to_Server():
	try:

		if(os.path.isfile('received')):
			return

		desiredSize = 128
		port = 55555
		time.sleep(1)
		#Create path if not existing
		slicePath = preTemp+"predictSlice\\";
		if not os.path.exists(os.path.dirname(slicePath)):
			try:
				os.makedirs(os.path.dirname(slicePath))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise

		if isMono(file):
			command = 'cp "{}" "{}.mp3"'.format(file,preTemp+newFilename)
		else:
			command = 'sox "{}" "{}.mp3" remix 1,2'.format(file,preTemp+newFilename)
		p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False, cwd=currentPath)
		output, errors = p.communicate()
		if errors:
			print (errors)

		#Create spectrogram
		command = 'sox "{}.mp3" -n spectrogram -Y 200 -X {} -m -r -o "{}.png"'.format(preTemp+newFilename,pixelPerSecond,preTemp+newFilename)
		p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False, cwd=currentPath)
		output, errors = p.communicate()
		if errors:
			print (errors)

		#Remove tmp mono track
		if os.path.exists("{}.mp3".format(preTemp+newFilename)):
			os.remove("{}.mp3".format(preTemp+newFilename))

		# Load the full spectrogram
		img = Image.open(preTemp+newFilename+".png")

		#Compute approximate number of 128x128 samples
		width, height = img.size
		nbSamples = int(width/desiredSize)
		width - desiredSize

		#For each sample
		for i in range(nbSamples):
			#Extract and save 128x128 sample
			startPixel = i*desiredSize
			imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
			imgTmp.save(slicePath+"{}/{}_{}.png".format("",newFilename[:-4],i))
		print ("Slices Created... ")

		# Create Array
		nbClasses = 13
		filenames = os.listdir(slicePath)
		print (filenames)
		data = []
		trainNb = 0
		for filename in filenames:
			imgData = getImageData(slicePath+"/"+filename, sliceSize)
			data.append((imgData))
			trainNb = trainNb + 1


		print ("FEED_DATA #############################################################")
		feedData = np.array(data[:trainNb]).reshape([-1, sliceSize, sliceSize, 1])
		print(feedData)
		datatosend = feedData.tolist()

		print ("data_arr created ..........")
		print ("sending data ....")

		s=socket.socket()
		hostname = socket.gethostbyname('baap')
		s.connect((hostname, port))
		data = s.send(pickle.dumps(datatosend))
		s.shutdown(socket.SHUT_WR)


		print("slices ready to rock!!!")


		print("data send")


		f = open('file2send','wb') # Open in binary

		l = s.recv(1024)
		timeout = time.time() + 10   # 5 minutes from now
		while (l):
			print ("Receiving...")
			f.write(l)
			l = s.recv(1024)
		f.close()
		os.rename('file2send', 'received')
		s.close()
		print("Receivied")
		

	except Exception as e:
		print (e)
		raise
		return

def main():
	
	try:
		threading.Thread(target=Start_Playback, args=()).start()
		start_new_thread (Send_File_to_Server, ())

	except Exception as e:
		print (e)

if __name__ == "__main__":
	main()



