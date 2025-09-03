"""
file for genome class
tasks:
1. initializing weights
2. crossover between self and other instance of class
3. mutation based on fitness
"""
import random
import math
from settings import *


class Genome():
    def __init__(self, weights=None):
        self.layer_sizes = [len(SENSOR_ANGLES), NUM_HIDDEN_LAYERS, 2] # size of each layer of neural network
        self.num_weights = (self.layer_sizes[0] * self.layer_sizes[1]) + (self.layer_sizes[1] * self.layer_sizes[2])

        if weights: # assign weights if provided
            self.weights = weights
        else: # random weights if not provided
            self.weights = self.random_weights()


    def random_weights(self):
        rand_weights = [random.uniform(-1, 1) for _ in range(self.num_weights)]
        return rand_weights


    def crossover(self, genome):
        # average weights of parents
        child_weights = []
        for i in range(self.num_weights):
            child_weight = (self.weights[i] + genome.weights[i]) / 2
            child_weights.append(child_weight)
        
        child_genome = Genome(child_weights) # create child's genome with crossover weights
        return child_genome


    def mutate(self, best_fitness, generation):
        # exponential decay based on generation
        mutation_mag = INITIAL_MUT_MAG * math.exp(-DECAY_RATE * generation)

        # scale inversely to fitness
        fitness_factor = max(0.1, 1.0 / (1.0 + best_fitness * FITNESS_SCALE))
        mutation_mag *= fitness_factor

        for i in range(self.num_weights):
            if random.random() < MUT_RATE: # mutate random number of weights
                random_mutation = random.gauss(0, mutation_mag)
                new_weight = self.weights[i] + random_mutation
                self.weights[i] = max(-MAX_WEIGHT, min(MAX_WEIGHT, new_weight)) # make sure weights don't exceed max threshold