import pygame

# Settings
TRACK_COLOR = (150, 150, 150)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 120

######################################################################################
# Environment
######################################################################################


class Environment:
    def __init__(self):
        self.track_segments = [] # list of track segments
        self.make_track()


    def add_segment(self, x, y, angle_deg=0, width=10, height=100):
        """
        angle_deg: 0 (vertical), 90 (horizontal), 45 or -45 only
        """
        surf = pygame.Surface((width, height), pygame.SRCALPHA) # create surface object for rectangle
        surf.fill(TRACK_COLOR)

        rotated_surf = pygame.transform.rotate(surf, -angle_deg) # rotate rectangle
        rect = rotated_surf.get_rect(center=(x, y)) # rect for rotated rectangle (area that the shape takes up)
        mask = pygame.mask.from_surface(rotated_surf) # outline of shape (for collision detection)

        # add rectangle information to list
        self.track_segments.append({
            "surface": rotated_surf,
            "rect": rect,
            "mask": mask
        })

    def make_track(self):
        self.add_segment(100, 100, 45, 20, 200)
        self.add_segment(200, 200, 0, 20, 200)


    def draw(self, screen):
        # Draw the track
        for segment in self.track_segments:
            screen.blit(segment["surface"], segment["rect"])


    def is_on_track(self, car_surface, car_rect):
        car_mask = pygame.mask.from_surface(car_surface) # create mask for car

        for segment in self.track_segments:
            offset = (segment["rect"].x - car_rect.x, segment["rect"].y - car_rect.y) # determine offset
            if car_mask.overlap(segment["mask"], offset): # check for collision
                return True
        return False
    

######################################################################################
# Initialization
######################################################################################

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create window object
pygame.display.set_caption("Cars")
clock = pygame.time.Clock() # initialize clock to manage frame rate
font = pygame.font.SysFont(None, 36)
pygame.mouse.set_visible(False)

env = Environment() # object for environment display


######################################################################################
# Main loop
######################################################################################

def main():
    cursor = pygame.Surface((30, 30))

    running = True # enter main loop

    while running:
        screen.fill((30, 30, 30)) # fill background gray

        # events (user input)
        for event in pygame.event.get(): # check if program is quit
            if event.type == pygame.QUIT:
                running = False

        # loop (computation)
        pos = pygame.mouse.get_pos() # get mouse coords
        cursor_rect = pygame.Rect(pos[0], pos[1], 30, 30)

        # render (display screen)
        env.draw(screen)
        if env.is_on_track(cursor, cursor_rect):
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        cursor.fill(color)
        screen.blit(cursor, pos)

        pygame.display.flip()
        clock.tick(FPS) # keeps loop at 120 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

