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


#Define
currentPath = os.path.dirname(os.path.realpath(__file__)) 
file = "test.mp3"
newFilename = "testmono"
desiredSize = 128

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
# if os.path.exists("{}.mp3".format(preTemp+newFilename)):
# 	os.remove("{}.mp3".format(preTemp+newFilename))


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



# array
nbClasses = 13
filenames = os.listdir(slicePath)
print (filenames)
data = []
trainNb = 0
for filename in filenames:
    imgData = getImageData(slicePath+"/"+filename, sliceSize)
    data.append((imgData))
    trainNb = trainNb + 1

feedData = np.array(data[:trainNb]).reshape([-1, sliceSize, sliceSize, 1])

print(feedData)
 

model = createModel(nbClasses, sliceSize)
print ("Model Created")
model.load('musicDNN.tflearn')

print ("++++++++++++++++++++++++++++++++++++",data[14],"+++++++++++++++++++++++++++++++++++++")

results = model.predict(feedData)
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
np.set_printoptions(threshold=np.inf)

print (results)

print("EOP!!!")