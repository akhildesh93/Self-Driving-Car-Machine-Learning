# -*- coding: utf-8 -*-
"""Traffic Signs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CrlOUE7tu1TJ2zMX_YFJiw1TqgQyoqet
"""

!git clone https://bitbucket.org/jadslim/german-traffic-signs

!ls german-traffic-signs/

import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical
from keras.layers import Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
import pickle #can be serialized before writing to file, converts to a character stream
import pandas as pd
import random

np.random.seed(0)

with open('german-traffic-signs/train.p', 'rb') as f: #rb binary format
  train_data = pickle.load(f)
with open('german-traffic-signs/valid.p', 'rb') as f: #rb binary format
  val_data = pickle.load(f)
with open('german-traffic-signs/test.p', 'rb') as f: #rb binary format
  test_data = pickle.load(f)

X_train, y_train = train_data['features'], train_data['labels']
X_val, y_val = val_data['features'], val_data['labels']
X_test, y_test = test_data['features'], test_data['labels']

print(X_train.shape)
print(X_val.shape)
print(X_test.shape) #traffic signs are in rgb, so have depth of 3 and 32x32

data = pd.read_csv('german-traffic-signs/signnames.csv')

num_of_samples=[]
cols = 5 #can be any number to show
num_classes = 43 #10 numbers

fig, axs = plt.subplots(nrows=num_classes, ncols=cols, figsize=(5,50))
fig.tight_layout()

for i in range(cols):
  for j, row in data.iterrows():
    x_selected = X_train[y_train==j]
    axs[j][i].imshow(x_selected[random.randint(0,(len(x_selected) - 1)), :, :], cmap=plt.get_cmap('gray')) #showing random num from number
    axs[j][i].axis("off") #making it look less crowded
    if i == 2:
      axs[j][i].set_title(str(j) + "-" + row["SignName"])
      num_of_samples.append(len(x_selected)) #find out # of numbers

print(num_of_samples)
plt.figure(figsize=(12, 4))
plt.bar(range(num_classes), num_of_samples)
plt.title("Training set")
plt.xlabel("Number")
plt.ylabel("# images")
plt.show()

import cv2

plt.imshow(X_train[1000])
plt.axis("off")
print(X_train[1000].shape)
print(y_train[1000])

def grayscale(img):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  return img

img = grayscale(X_train[1000])
plt.imshow(img)
print(img.shape)

#histogram equalization, normalizes brightness, enhances contrast
def equalize(img):
  img = cv2.equalizeHist(img)
  return img

img = equalize(img)
plt.imshow(img)

def preprocessing(img):
  img = grayscale(img)
  img = equalize(img)
  img = img/255 #normalize
  return img

X_train = np.array(list(map(preprocessing, X_train))) #loops through all of X_train and preprocesses
X_val = np.array(list(map(preprocessing, X_val))) 
X_test = np.array(list(map(preprocessing, X_test)))

plt.imshow(X_train[random.randint(0, len(X_train)-1)])
plt.axis("off")
print(X_train.shape)

#adds depth of 1 for CNN
X_train = X_train.reshape(34799, 32, 32, 1)
X_val = X_val.reshape(4410, 32, 32, 1)
X_test = X_test.reshape(12630, 32, 32, 1)

#data augmentation, making changes to data like zooming and rotating and adding as new data
#helps categories with less data

from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(width_shift_range=0.1, 
                              height_shift_range=0.1, 
                              zoom_range=0.2,
                              shear_range=0.1,
                              rotation_range=10.)
datagen.fit(X_train)

batches = datagen.flow(X_train, y_train, batch_size=20)
X_batch, y_batch = next(batches)

fig, axs = plt.subplots(1, 15, figsize=(20,5))
fig.tight_layout()

for i in range(15):
  axs[i].imshow(X_batch[i].reshape(32,32))
  axs[i].axis("off")

y_train = to_categorical(y_train, 43)
y_val = to_categorical(y_val, 43)
y_test = to_categorical(y_test, 43)

def leNet_model():
  model = Sequential()
    #num of filters, size of filter
  model.add(Conv2D(60, (5,5), input_shape=(32,32,1), activation='relu'))
  model.add(Conv2D(60, (5,5), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2,2))) 

  model.add(Conv2D(30, (3,3), activation='relu'))
  model.add(Conv2D(30, (3,3), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2,2))) #scales down feature maps by 1/2
  
  #model.add(Dropout(0.5))

  model.add(Flatten())
    # num of nodes
  model.add(Dense(500, activation='relu'))
  model.add(Dropout(0.5))
  
  model.add(Dense(num_classes, activation='softmax'))
  
  model.compile(Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
  return model

model = leNet_model()
model.summary()

#fit_generator allows generator to be run 
history = model.fit_generator(datagen.flow(X_train, y_train,
                              batch_size=50),
                              steps_per_epoch=X_train.shape[0]/50,
                              epochs=15,
                              validation_data=(X_val, y_val),
                              shuffle=1)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['training', 'validation'])
plt.title('Loss')
plt.xlabel('epoch')

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['training', 'validation'])
plt.title('Accuracy')
plt.xlabel('epoch')

score = model.evaluate(X_test, y_test, verbose=0)
print("Test score: ", score[0])
print("Test accuracy: ", score[1])

#fetch image
import requests
from PIL import Image
url = 'https://c8.alamy.com/comp/G667W0/road-sign-speed-limit-30-kmh-zone-passau-bavaria-germany-G667W0.jpg'
r = requests.get(url, stream=True)
img = Image.open(r.raw)
plt.imshow(img, cmap=plt.get_cmap('gray'))

#preprocess image
img = np.asarray(img)
img = cv2.resize(img, (32, 32))
img = preprocessing(img)
plt.imshow(img, cmap=plt.get_cmap('gray'))
print(img.shape)

#add depth of 1
img = img.reshape(1, 32, 32, 1)

#test image
prediction = np.argmax(model.predict(img), axis=1)
print("Predicted sign: " + str(prediction))

"""https://c8.alamy.com/comp/G667W0/road-sign-speed-limit-30-kmh-zone-passau-bavaria-germany-G667W0.jpg

https://c8.alamy.com/comp/A0RX23/cars-and-automobiles-must-turn-left-ahead-sign-A0RX23.jpg

https://previews.123rf.com/images/bwylezich/bwylezich1608/bwylezich160800375/64914157-german-road-sign-slippery-road.jpg

https://previews.123rf.com/images/pejo/pejo0907/pejo090700003/5155701-german-traffic-sign-no-205-give-way.jpg

https://c8.alamy.com/comp/J2MRAJ/german-road-sign-bicycles-crossing-J2MRAJ.jpg
"""