import os
from config import preTemp

slicePath = preTemp+"predictSlice\\";
filenames = os.listdir(slicePath)
print (filenames)