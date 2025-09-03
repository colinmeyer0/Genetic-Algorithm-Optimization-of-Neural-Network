"""
population class
including:
1. 
"""
import pygame
from settings import *
from agent import Agent
from genome import Genome
import random


class Population:
    def __init__(self):
        self.generation = 1
        self.agents = [Agent(Genome()) for _ in range(POP_SIZE)] # create initial generation


    def update_agents(self, env, screen, iterations):
        self.fitnesses = []
        for i in range(POP_SIZE):
            self.agents[i].update(env, screen, iterations)
            self.fitnesses.append(self.agents[i].fitness)

        self.select() # determine best agents


    def all_dead(self):
        return all(not agent.alive for agent in self.agents)


    def evolve(self):
        self.select() # select best agents from generation
        
        offspring = []
        for _ in range(POP_SIZE):
            parents = random.sample(self.best_agents, 2) # select 2 random parents
            child_genome = parents[0].genome.crossover(parents[1].genome) # crossover genes
            child_genome.mutate(self.best_agents[0].fitness, self.generation) # create random mutation in genes
            offspring.append(Agent(child_genome))

        # replace generation
        self.agents = offspring
        self.generation += 1


    def select(self):
        self.agents.sort(key=lambda agent: agent.fitness, reverse=True) # sort by fitness
        self.best_agents = self.agents[:NUM_PARENTS]

        self.furthest_agents = sorted(self.agents, key=lambda agent: agent.distance, reverse=True) # sort by distance (for camera offset)