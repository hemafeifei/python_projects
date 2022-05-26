#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This code can be used to generate raw_npz and embedded npz file.


from matplotlib import pyplot as plt
from PIL import Image
from os import listdir
from mtcnn.mtcnn import MTCNN

from numpy import load
from numpy import asarray
from numpy import expand_dims
from numpy import savez_compressed
from numpy import reshape
from keras.models import load_model

#Method to extract Face
detector = MTCNN()                  #assign the MTCNN detector
def extract_image(image):
    print(image)
    img1 = Image.open(image)            #open the image
    img1 = img1.convert('RGB')          #convert the image to RGB format
    pixels = asarray(img1)              #convert the image to numpy array
    f = detector.detect_faces(pixels)
    #fetching the (x,y)co-ordinate and (width-->w, height-->h) of the image
    x1,y1,w,h = f[0]['box']
    x1, y1 = abs(x1), abs(y1)
    x2 = abs(x1+w)
    y2 = abs(y1+h)
    #locate the co-ordinates of face in the image
    store_face = pixels[y1:y2,x1:x2]
    plt.imshow(store_face)
    image1 = Image.fromarray(store_face,'RGB')    #convert the numpy array to object
    image1 = image1.resize((160,160))             #resize the image
    face_array = asarray(image1)                  #image to array
    return face_array


#Method to fetch the face
def load_faces(directory):
    face = []
    i=1
    for filename in listdir(directory) :
        if not filename.startswith('.DS_Store'):
            path = directory + filename
            faces = extract_image(path)
            face.append(faces)
    return face


#Method to get the array of face data(trainX) and it's labels(trainY)
def load_dataset(directory):
    x, y = [],[]
    i=1
    for subdir in listdir(directory):
        path = directory + subdir + '/'
        #load all faces in subdirectory
        faces = load_faces(path)
        #create labels
        labels = [subdir for _ in range(len(faces))]
        #summarize
        print("%d There are %d images in the class %s:"%(i,len(faces),subdir))
        x.extend(faces)
        y.extend(labels)
        i=i+1
    return asarray(x),asarray(y)


#load the datasets
trainX,trainY = load_dataset('data/cv/indian_example/Indian-celebrities/')
print(trainX.shape,trainY.shape)
#compress the data
savez_compressed('data/cv/indian_example/Indian-celeb-dataset.npz',trainX,trainY)



#Generalize the data and extract the embeddings
def extract_embeddings(model, face_pixels):
    face_pixels = face_pixels.astype('float32')  #convert the entire data to float32(base)
    mean = face_pixels.mean()                    #evaluate the mean of the data
    std  = face_pixels.std()                     #evaluate the standard deviation of the data
    face_pixels = (face_pixels - mean) / std
    samples = expand_dims(face_pixels, axis=0)    #expand the dimension of data
    yhat = model.predict(samples)
    return yhat[0]

#load the compressed dataset and facenet keras model
data = load('data/cv/indian_example/Indian-celeb-dataset.npz')
trainx, trainy = data['arr_0'],data['arr_1']
print(trainx.shape, trainy.shape)
model = load_model('data/cv/indian_example/facenet_keras.h5')

#get the face embeddings
new_trainx = list()
for train_pixels in trainx:
    embeddings = extract_embeddings(model,train_pixels)
    new_trainx.append(embeddings)
new_trainx = asarray(new_trainx)             #convert the embeddings into numpy array
print(new_trainx.shape)

#compress the 128 embeddings of each face
savez_compressed('data/cv/indian_example/Indian-celeb-embeddings.npz',new_trainx,trainy)