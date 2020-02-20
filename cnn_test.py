import tensorflow as tf
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data

minst = input_data.read_data_sets("MNIST_DATA/", one_hot=True)