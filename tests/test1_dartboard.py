import pygame, sys, numpy as np


######################################################################################
# Initialization
######################################################################################

width, height = 1000, 1000
center = (width//2, height//2)
bullseye_radius = 7

pygame.init()
screen = pygame.display.set_mode((width, height)) # create window object
pygame.display.set_caption("Dartboard")
clock = pygame.time.Clock() # initialize clock to manage frame rate
font = pygame.font.SysFont(None, 36)


######################################################################################
# Genetic Algorithm
######################################################################################

# Create initial population
def create_population(size):
    return np.random.randint(0, 1000, (size, 2))


# Evaluate fitness (dummy example)
def fitness(individual):
    return distance(individual[0], individual[1], center[0], center[1])


def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**0.5


# Select the top N individuals
def select(population, scores, num_parents):
    sorted_indices = np.argsort(scores)
    return population[sorted_indices[:num_parents]]


# Crossover and mutation
def crossover(parents, offspring_size, avg_score):
    offspring = []
    rand_bounds = avg_score / 2
    for _ in range(offspring_size):
        p1, p2 = parents[np.random.randint(len(parents))], parents[np.random.randint(len(parents))]
        child = (p1 + p2) / 2
        child += np.random.normal(0, rand_bounds, size=child.shape)  # mutation
        offspring.append(child)
    return np.array(offspring)


######################################################################################
# Dart Board
######################################################################################

def throw_dart(surface, x, y, rgb):
    pygame.draw.circle(surface, rgb, (x, y), 5)


def draw_dartboard(surface):
    # initialize variables
    colors = [(115, 155, 215), (80, 125, 190), (50, 95, 160), (30, 75, 135)]
    radii = [400, 270, 140, bullseye_radius]

    # draw board
    screen.fill((255, 255, 255))
    for i in range(len(radii)):
        pygame.draw.circle(surface, colors[i], center, radii[i], 0)


def check_intersections(population, population_colors):
    for i in range(len(population)):
        if distance(population[i][0], population[i][1], center[0], center[1]) <= bullseye_radius:
            population_colors[i] = (0, 255, 0)


def all_green(population_colors):
    for color in population_colors:
        if color != (0, 255, 0):
            return False
    return True


def main():
    # generate darts
    pop_size = 40
    num_gen = 100
    generation = 0
    population = create_population(pop_size)
    population_colors = [(255, 0, 0) for _ in range(pop_size)] # set population colors

    running = True # enter main loop

    while running:
        # check if program is quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_dartboard(screen) # draw board

        check_intersections(population, population_colors)

        for i in range(len(population)):
            throw_dart(screen, population[i][0], population[i][1], population_colors[i])

        generation_num_text = font.render(f"Generation: {generation}", True, (0, 0, 0))
        screen.blit(generation_num_text, (10, 10))

        scores = np.array([fitness(ind) for ind in population]) # determine fitness
        parents = select(population, scores, 4) # select parents
        avg_score = sum(scores) / 40 # average score of population
        population = crossover(parents, len(population), avg_score) # create next generation
        generation += 1 # update generation count

        pygame.display.flip()
        clock.tick(2)  # keeps loop at 60 FPS

        if generation >= num_gen or all_green(population_colors):
            running = False

        population_colors = [(255, 0, 0) for _ in range(pop_size)] # reset population colors

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

