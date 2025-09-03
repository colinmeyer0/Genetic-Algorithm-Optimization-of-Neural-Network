"""
file for neural network class
including:
1. processing inputs
2. normalizing using activation function
"""
from settings import *
import math


class NeuralNetwork:
    def __init__(self, layer_sizes, weights):
        self.layer_sizes = layer_sizes # size of each layer
        self.weights = weights


    def feedforward(self, inputs:list):
        idx = 0
        current_layer = inputs.copy() # current layer being calculated

        for layer_i in range(len(self.layer_sizes) - 1): # iterate through layers
            next_layer = []
            input_size = self.layer_sizes[layer_i] # current layer size
            output_size = self.layer_sizes[layer_i + 1] # next layer size

            for out_i in range(output_size): # iterate through each next layer node
                total = 0

                for inp_i in range(input_size): # iterate through each current node
                    total += current_layer[inp_i] * self.weights[idx] # weight output sum for next layer node
                    idx += 1

                activated_total = self.activate(total)
                next_layer.append(activated_total)

            current_layer = next_layer

        return current_layer


    def activate(self, sum):
        tanh = (math.exp(sum) - math.exp(-sum)) / (math.exp(sum) + math.exp(-sum)) # activate total using tanh (range: (-1, 1))
        return tanh