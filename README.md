This is a Self Driving Car Simulation based on a vehicle simulation from https://github.com/udacity/self-driving-car-sim.

Watch the demo (self-driving-car-demo.mp4)

IMG/
  - contains image files of training data
  - used simulator from https://github.com/udacity/self-driving-car-sim
  - obtained data from manually driving through Course 1 (training)

driving-log.csv
  - contains info about each image (steering angle utilized)

behavior-cloning.py
  - uses training data to create a Convolutional Neural Network
  - Neural Network architecture structured from NVIDIA CNN for lane lines

    Algorithmic steps:
      - augments data with generator (zoom, brightening, pan, flip)
      - preprocesses data
      - NVIDIA Convolutional Neural Network
      - trains model (train/validation split)
      - downloads model

Model successfully generalizes and car autonomously drives through Course 2 (testing)

traffic_signs_cnn.py
  - Convolutional Neural Network to identify road signs
  - Performs at 97.2% accuracy on test set
