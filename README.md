IMG/
  - contains image files of training data
  - used simulator from https://github.com/udacity/self-driving-car-sim
  - obtained data from manually driving through Course 1 (training)

driving-log.csv
  - contains info about each image (steering angle utilized)

behavior-cloning.py
  -uses training data to create a Convolutional Neural Network
  -Neural Network architecture structured from NVIDIA CNN for lane lines

  Machine Learning steps:
    - augments data with generator (zoom, brightening, pan, flip)
    - preprocesses data
    - NVIDIA Convolutional Neural Network
    - trains model
    - downloads model

