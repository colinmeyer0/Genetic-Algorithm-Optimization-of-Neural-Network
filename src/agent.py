"""
file for agent class
tasks:
1. checking obstacle collision bounds
2. updating position based on feedforward neural network
3. determining fitness based on speed and distance
4. displaying agent to window
"""
import pygame
from settings import *
from environment import Environment
from genome import Genome
from neural_network import NeuralNetwork
import math


class Agent():
    def __init__(self, genome:Genome):
        # initialize attributes
        self.genome = genome
        self.network = NeuralNetwork(genome.layer_sizes, genome.weights)

        self.position = pygame.Vector2(AGENT_START)
        self.angle = 90
        self.distance = 0
        self.fitness = 0
        self.alive = True

        # template surface to copy
        self.original_surface = pygame.Surface((AGENT_WIDTH, AGENT_HEIGHT), pygame.SRCALPHA)
        self.original_surface.fill(AGENT_ALIVE_COLOR)

        # initial surface
        self.surface = pygame.transform.rotate(self.original_surface, -self.angle)
        self.rect = self.surface.get_rect(center=(self.position.x, self.position.y))
        self.mask = pygame.mask.from_surface(self.surface)


    def update(self, env:Environment, screen, iterations):
        # check if alive
        if not self.alive:
            return
        
        # retrieve genome response
        sensor_readings = self.sense_environment(env, screen)
        self.evaluate_data(sensor_readings) # scale NN outputs to car movement parameters

        # update speed (pixels/s) and angle (degrees)
        self.angle += self.angular_velocity

        # update position
        self.position.x += math.cos(math.radians(self.angle)) * self.speed
        self.position.y += math.sin(math.radians(self.angle)) * self.speed

        self.check_bounds(env) # check if alive
        self.calculate_fitness(iterations)

        # determine surface, rect, and mask
        self.surface = pygame.transform.rotate(self.original_surface, -self.angle)
        self.rect = self.surface.get_rect(center=(self.position.x, self.position.y))
        self.mask = pygame.mask.from_surface(self.surface)


    def evaluate_data(self, sensor_readings):
        speed_output, ang_vel_output = self.network.feedforward(sensor_readings) # get NN outputs

        self.speed = (speed_output + 1) / 2 * (MAX_SPEED - MIN_SPEED) + MIN_SPEED # map [-1,1] to [min_speed,max_speed]
        self.angular_velocity = ang_vel_output * MAX_ANG_VEL


    def check_bounds(self, env:Environment):
        # determine if car is within window
        if self.position.x < 0 or self.position.x > WORLD_WIDTH or self.position.y < 0 or self.position.y > WORLD_HEIGHT:
            self.alive = False
            self.original_surface.fill(AGENT_DEAD_COLOR)

        # determine if car collides with track
        elif not env.is_on_track(self.surface, self.rect):
            self.alive = False
            self.original_surface.fill(AGENT_DEAD_COLOR)


    def sense_environment(self, env:Environment, screen):
        distances, self.sensor_points = env.cast_all_rays(self.position, self.angle)

        return distances


    def calculate_fitness(self, iterations):
        self.distance += self.speed # update distance traveled
        avg_speed = self.distance / iterations
        
        # normalize speed and distance to fraction of 1.0
        norm_distance = self.distance / TRACK_LENGTH
        norm_avg_speed = avg_speed / MAX_SPEED
        
        self.fitness = norm_distance * DIST_WEIGHT + norm_avg_speed * AVG_SPEED_WEIGHT # calculate fitness


    def draw(self, screen:pygame.Surface, camera_offset):
        # draw agent
        offset_rect = self.rect.move(-camera_offset.x, -camera_offset.y)
        screen.blit(self.surface, offset_rect)

        # draw sensor points
        for point in self.sensor_points:
            offset_point = point - camera_offset
            pygame.draw.circle(screen, SENSOR_COLOR, offset_point, 5)