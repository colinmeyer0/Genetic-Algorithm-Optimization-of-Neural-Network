import pygame
import json

# settings
WORLD_WIDTH, WORLD_HEIGHT = 3200, 1800 # dimensions of window
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900 # dimensions of entire world/course
SCROLL_RATE = 5 # pxls/s
SEGMENT_WIDTH = 10
SEGMENT_HEIGHT = 100
ANGLES = [0, 30, 60, 90, 120, 150]
BG_COLOR = (30, 30, 30)
TRACK_COLOR = (255, 255, 255)

# initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
camera_offset = pygame.Vector2(0, 0)




# Draw text
def draw_text(text, x, y):
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))


# Main loop
def main():
    current_angle_index = 0
    segments = []  # List of dicts with x, y, angle, height, width
    screen_center = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    running = True
    while running:
        screen.fill(BG_COLOR)

        # move window
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and screen_center.y >= SCREEN_HEIGHT // 2 - SCROLL_RATE: screen_center.y -= SCROLL_RATE
        if keys[pygame.K_a] and screen_center.x >= SCREEN_WIDTH // 2 - SCROLL_RATE: screen_center.x -= SCROLL_RATE
        if keys[pygame.K_s] and screen_center.y <= WORLD_HEIGHT - SCREEN_HEIGHT // 2 + SCROLL_RATE: screen_center.y += SCROLL_RATE
        if keys[pygame.K_d] and screen_center.x <= WORLD_WIDTH - SCREEN_WIDTH // 2 + SCROLL_RATE: screen_center.x += SCROLL_RATE
        
        # calculate offset
        camera_offset.x = screen_center.x - SCREEN_WIDTH // 2
        camera_offset.y = screen_center.y - SCREEN_HEIGHT // 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # rotate track
                if event.key == pygame.K_RIGHT:
                    current_angle_index = (current_angle_index + 1) % len(ANGLES)
                elif event.key == pygame.K_LEFT:
                    current_angle_index = (current_angle_index - 1) % len(ANGLES)

                # Save to file
                elif event.key == pygame.K_f:
                    with open("track.json", "w") as file:
                        json.dump(segments, file, indent=4)
                    print("Track saved to track.json")

            # track placed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    offset_x = x + camera_offset.x
                    offset_y = y + camera_offset.y
                    angle = ANGLES[current_angle_index]
                    segments.append({"x": offset_x, "y": offset_y, "angle": angle, "height": SEGMENT_HEIGHT, "width": SEGMENT_WIDTH})



        # Draw all segments
        for seg in segments:
            surf = pygame.Surface((SEGMENT_WIDTH, SEGMENT_HEIGHT), pygame.SRCALPHA)
            surf.fill(TRACK_COLOR)
            rotated = pygame.transform.rotate(surf, -seg["angle"])
            rect = rotated.get_rect(center=(seg["x"], seg["y"]))
            offset_rect = rect.move(-camera_offset.x, -camera_offset.y)
            screen.blit(rotated, offset_rect.topleft)

        # Draw preview at mouse
        mx, my = pygame.mouse.get_pos()
        angle = ANGLES[current_angle_index]
        preview = pygame.Surface((SEGMENT_WIDTH, SEGMENT_HEIGHT), pygame.SRCALPHA)
        preview.fill((150, 150, 150))
        rotated_preview = pygame.transform.rotate(preview, -angle)
        preview_rect = rotated_preview.get_rect(center=(mx, my))
        screen.blit(rotated_preview, preview_rect.topleft)

        draw_text(f"Angle: {angle}", 10, 10)
        draw_text("[Click] to add, [Left/Right] to change angle, [F] to save", 10, 30)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()