import numpy as np
import cv2
import os
import glob
import time

data = []
## path of the image file
path = 'output/seg'

## color map instruction
label_value = [[0,0,0],[70,70,70],[153,153,190],[160, 170, 250],[60, 20, 220],[153, 153, 153],[50, 234, 157],[128, 64, 128],[232, 35, 244],[35, 142, 107],[142, 0, 0],[156, 102, 102],[0, 220, 220]]
label_class = ['Unlabeled','Building','Fence','Other','Pedestrian','Pole','Road line','Road','Sidewalk','Vegetation','Car','Wall','Traffic sign']


## reading the data from image
for filename in glob.glob(path+'/*.png'):
	img = cv2.imread(filename,cv2.IMREAD_COLOR)
	data.append(img)

data = np.array(data)
print(data.shape)

result_ = []

## sorting out rgb values of each pixel,result is 2d array with each pixel's rgb value
for i in range(data.shape[0]):
	for j in range(data.shape[1]):
		for k in range(data.shape[2]):
			result_.append(data[i,j,k])

## getting unique set of pixel values 
class_pixels = np.unique(result_,axis = 0,return_counts = True)
class_pixels_value,class_pixels_count = np.array(class_pixels[0]).tolist(),np.array(class_pixels[1]).tolist()

print(class_pixels)
class_counts = {}

## comparing with color map info to get their corresponding classes and counts
for val1 in class_pixels_value:
	for val2 in label_value:
		comp = map(lambda x,y: abs(x-y), val1,val2)
		if max(comp) == 0:
			i,j = class_pixels_value.index(val1),label_value.index(val2)
			## if both --> unique and label pixels values are equal, then using their index values to get corresponding classses and counts
			class_counts.update({label_class[j]:class_pixels_count[i]})


print(class_counts)


