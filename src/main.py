"""
main control loop and initialization
"""
import pygame
from settings import *
from environment import Environment
from population import Population


######################################################################################
# Initialization
######################################################################################

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create window object
pygame.display.set_caption("Cars")
clock = pygame.time.Clock() # initialize clock to manage frame rate
font = pygame.font.SysFont(None, 25)
camera_offset = pygame.Vector2(0, 0)

env = Environment() # object for environment display
pop = Population() # create population

######################################################################################
# Main loop
######################################################################################

def main():
    running = True # enter main loop
    iterations = 1 # number of iterations (ticks) for a given generation

    while running:
        screen.fill(BG_COLOR) # fill background gray

        # events (user input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # check if program is quit
                running = False
            # elif event.type == pygame.KEYDOWN: # check if key is pressed

        # loop (computation)
        pop.update_agents(env, screen, iterations)
        update_camera()

        # render (display screen)
        for agent in pop.agents:
            agent.draw(screen, camera_offset)
        env.draw(screen, font, pop, camera_offset)

        # check for evolution
        if pop.all_dead():
            pop.evolve()
            iterations = 0 # reset iteration count

        pygame.display.flip()
        clock.tick(FPS) # keeps loop at 100 FPS
        iterations += 1

    pygame.quit()


def update_camera():
    camera_center = (pop.furthest_agents[0].rect.center) # center camera on best agent

    camera_offset.x = camera_center[0] - SCREEN_WIDTH // 2
    camera_offset.y = camera_center[1] - SCREEN_HEIGHT // 2
    camera_offset.x = max(0, min(camera_offset.x, WORLD_WIDTH - SCREEN_WIDTH))
    camera_offset.y = max(0, min(camera_offset.y, WORLD_HEIGHT - SCREEN_HEIGHT))


if __name__ == "__main__":
    main()