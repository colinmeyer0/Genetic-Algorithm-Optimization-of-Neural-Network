# Genetic-Algorithm-Optimization-of-Neural-Networks

A 2D simulation framework built in Python/PyGame where autonomous agents (cars) learn to drive using an **evolutionary genetic algorithm** to train the weights of a **feedforward neural network**. The system demonstrates emergent navigation behavior as agents learn to optimize distance traveled and maintain the highest average speed while avoiding collisions.

![](media/demo.gif)

## Overview
Agents must navigate the track without colliding with track segments. The agents have three ray casting sensors, providing distance measurements to the nearest obstacle in a given direction. Each car is controlled by a standard feedforward neural network with three layers: an input layer with three neurons, a hidden layer with six neurons, and an output layer with two neurons. The distance sensors serve as the inputs of the network's first layer, the output layer returns the agent's steering and throttle response. A genetic algorithm optimizes these neural networks through selection over generations to improve driving performance.

The simulation highlights concepts in:
- **Optimization:** fitness-based selection via an evolutionary genetic algorithm
- **Machine Learning:** feedforward neural network controllers
- **Bit masking:** pixel-perfect collision detection
- **Spatial Partitioning:** hash map for run-time optimization of N-body collision detection
- **Front-End GUI:** visualization of algorithm using PyGame

## Core Algorithms

### Genetic Algorithm
Each car’s control behavior is determined by a neural network with weights that form its genome. The GA evolves these genomes using:
- **Selection** – fitter agents are more likely to reproduce
- **Crossover** – offspring inherit a mix of weights from two parents
- **Mutation** – small random perturbations to weights, with mutation magnitude scaled inversely to the best fitness (behavior gets less randomization as performance improves)
- **Evolution** – repeated over many generations, producing agents that gradually improve navigation

### Feedforward Neural Network
- **Inputs**: Raycast distance sensors (front, 40 degrees to the left and right)
- **Hidden Layer**: Fully connected to input and output with 6 neurons
- **Outputs**: Angular velocity (steering) and acceleration (throttle)
- **Activation**: `tanh` function ensures **non-linear decision boundaries** and outputs normalized to [-1, 1]

## Simulation Features
#### Three-Phase Collision Detection
- **Spatial Partitioning (Broad Phase):** Track segments are bucketed into discrete cells of a hash map grid based on position. Collision checks are limited to objects sharing the same or neighboring cells, greatly reducing time complexity.
- **Bounding Box Check (Narrow Phase):** For each nearby segment, a quick rectangle intersection test is performed before performing pixel-perfect checks.
- **Pixel-Perfect Mask Collision (Precise Phase):** Exact collision detection using object bit masks.

#### Ray Casting
- Cars use multiple ray cast distance sensors to detect walls as inputs to the neural network controller.
- Implemented with vector math and line intersections.

#### Track Editor
- Supports interactive placement of segments using mouse input to create tracks.
- Save and load environment layouts as JSON files, enabling customization without modifying source code.

## Results
- Agents evolve from random, wall-crashing behavior to purposeful navigation after several generations.
- Once the end of the track is met, subsequent generations optimize performance to achieve superior lap times.
	- Eminent navigation behavior is demonstrated by acceleration in long straights and deceleration in corners.
- Mutation scaling ensures early exploration and later fine-tuning.

## Personal Note
This was my first large-scale programming project. My goal when I started this project was to step well outside of my comfort zone; I researched and implemented many advanced concepts I had no experience with. It has been an incredible learning experience in my development as a programmer, not only due to the skills I have attained but also because of how I have learned *how to learn*. My confidence in being able to approach complex challenges, ones that are completely foreign to me, has grown immensely. I am now certain of my ability to combine abstract goals with implementation.
