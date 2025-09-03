"""
file for settings, i.e. constant values that can be changed
"""
# main
WORLD_WIDTH, WORLD_HEIGHT = 3200, 1800 # dimensions of window
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900 # dimensions of entire world/course
FPS = 260
BG_COLOR = (30, 30, 30)

# environment
TRACK_COLOR = (150, 150, 150)
TRACK_LENGTH = 7000 # distance from start to finish (approximate)
FILE_NAME = "tracks/track3.json"
SENSOR_COLOR = (150, 150, 255)
TEXT_COLOR = (255, 255, 255)
GRID_SIZE = 150

# population
POP_SIZE = 10
NUM_GEN = 100
NUM_PARENTS = 2

# agent
AGENT_WIDTH = 35
AGENT_HEIGHT = 22
AGENT_START = (120, 50)
AGENT_ALIVE_COLOR = (0, 255, 0)
AGENT_DEAD_COLOR = (255, 0, 0)
SENSOR_ANGLES = (-45, 0, 45)
MAX_SENSOR_DIST = 250
MAX_ANG_VEL = 2
MAX_SPEED = 7
MIN_SPEED = 3
DIST_WEIGHT = 1
AVG_SPEED_WEIGHT = 0.3
RAY_STEP = 5

# genome
MUT_RATE = 0.4
MAX_WEIGHT = 1.0
INITIAL_MUT_MAG = 2
DECAY_RATE = 0.03
FITNESS_SCALE = 1.7


# NeuralNetwork
NUM_HIDDEN_LAYERS = 6