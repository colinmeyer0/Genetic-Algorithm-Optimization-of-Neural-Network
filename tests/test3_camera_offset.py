import pygame



"""
Constants
"""
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 # dimensions of window
WORLD_WIDTH, WORLD_HEIGHT = 4000, 3000 # dimensions of entire world/course


"""
Initialization
"""
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create window object
clock = pygame.time.Clock() # initialize clock to manage frame rate

player = pygame.Rect(100, 100, 50, 50)  # x, y, width, height
player_speed = 5
walls = [
    pygame.Rect(300, 300, 200, 50),
    pygame.Rect(800, 400, 100, 300),
    pygame.Rect(1500, 1200, 300, 300),
]
camera_offset = pygame.Vector2(0, 0)


"""
Main Logic
"""
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.y -= player_speed
        if keys[pygame.K_s]: player.y += player_speed
        if keys[pygame.K_a]: player.x -= player_speed
        if keys[pygame.K_d]: player.x += player_speed

        update_camera()
        draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def update_camera():
    camera_offset.x = player.centerx - SCREEN_WIDTH // 2
    camera_offset.y = player.centery - SCREEN_HEIGHT // 2
    camera_offset.x = max(0, min(camera_offset.x, WORLD_WIDTH - SCREEN_WIDTH))
    camera_offset.y = max(0, min(camera_offset.y, WORLD_HEIGHT - SCREEN_HEIGHT))


def draw():
    screen.fill((50, 50, 50))  # background

    # Draw walls with camera offset
    for wall in walls:
        wall_screen_pos = wall.move(-camera_offset.x, -camera_offset.y)
        pygame.draw.rect(screen, (200, 50, 50), wall_screen_pos)

    # Draw player
    player_screen_pos = player.move(-camera_offset.x, -camera_offset.y)
    pygame.draw.rect(screen, (50, 200, 50), player_screen_pos)


if __name__ == "__main__":
    main()