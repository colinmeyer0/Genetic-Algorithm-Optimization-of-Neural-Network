"""
file for environment class
including:
1. loading track data
2. converting track segment data to pygame surface objects
3. displaying the track to the window
4. track segment collision detection with car
5. spatial partitioning (constructing spatial grid)
6. casting sensor rays
7. rendering text to window
"""

import pygame
from settings import *
import math
import json



class Environment:
    def __init__(self):
        self.track_segments = [] # list of track segments
        self.grid = {} # dictionary of grid cells: (grid_x, grid_y)

        self._load_track(FILE_NAME)
        self._create_grid() # create spatial grid for track segments


    def _load_track(self, filename):
        # load json file data from track_editor.py
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            for seg in data:
                self._add_segment(seg["x"], seg["y"], seg["angle"], seg["height"], seg["width"])
            print(f"Loaded {len(data)} track segments from {filename}")

        except Exception as e:
            print(f"Error loading track: {e}")


    def _add_segment(self, x, y, angle=0, height=100, width=10):
        surf = pygame.Surface((width, height), pygame.SRCALPHA) # create surface object for rectangle
        surf.fill(TRACK_COLOR)

        rotated_surf = pygame.transform.rotate(surf, -angle) # rotate rectangle
        rect = rotated_surf.get_rect(center=(x, y)) # rect for rotated rectangle (area that the shape takes up)
        mask = pygame.mask.from_surface(rotated_surf) # outline of shape (for collision detection)

        # add rectangle information to list
        segment = {
            "surface": rotated_surf,
            "rect": rect,
            "mask": mask
        }
        self.track_segments.append(segment)


    def _create_grid(self):
        print("Building spatial grid...")

        for seg_idx, segment in enumerate(self.track_segments): # iterate through segments
            rect = segment["rect"]

            # find cell current segment overlaps
            left_cell = rect.left // GRID_SIZE
            right_cell = rect.right // GRID_SIZE
            top_cell = rect.top // GRID_SIZE
            bottom_cell = rect.bottom // GRID_SIZE

            for grid_x in range(left_cell, right_cell + 1):
                for grid_y in range(top_cell, bottom_cell + 1):
                    cell_key = (grid_x, grid_y)

                    # add cell to grid if it hasn't been added yet
                    if cell_key not in self.grid:
                        self.grid[cell_key] = []

                    self.grid[cell_key].append(seg_idx) # add segment to cell of grid that it's in

        print(f"Grid built with {len(self.grid)} cells")

    
    def is_on_track(self, car_surface:pygame.Surface, car_rect:pygame.Rect):
        car_mask = pygame.mask.from_surface(car_surface) # create mask for car
        nearby_segments = self._get_nearby_segments(car_rect) # determine which segments need to be checked for collision (nearby)

        for segment in nearby_segments:
            if not car_rect.colliderect(segment["rect"]):
                continue

            offset = (
                segment["rect"].x - car_rect.x,
                segment["rect"].y - car_rect.y
                ) # determine offset
            if car_mask.overlap(segment["mask"], offset): # check for collision
                return False # car collides with segment
            
        return True # car doesn't collide with segments
    

    def _get_nearby_segments(self, rect):
        # determine cells the car is contained in
        left_cell = rect.left // GRID_SIZE
        right_cell = rect.right // GRID_SIZE
        top_cell = rect.top // GRID_SIZE
        bottom_cell = rect.bottom // GRID_SIZE

        segment_indices = set() # set of nearby segment indices
        for grid_x in range(left_cell, right_cell + 1):
            for grid_y in range(top_cell, bottom_cell + 1):
                cell_key = (grid_x, grid_y)

                if cell_key in self.grid: # check if any segments are in cell
                    segment_indices.update(self.grid[cell_key]) # add segment indices from current cell to set

        return [self.track_segments[i] for i in segment_indices] # return nearby segments
    

    def cast_all_rays(self, agent_pos, agent_angle):
        distances = []
        collision_points = []

        # iterate each sensor angle
        for offset_angle in SENSOR_ANGLES:
            ray_angle = agent_angle + offset_angle
            
            dx = math.cos(math.radians(ray_angle))
            dy = math.sin(math.radians(ray_angle))
            dir_vec = pygame.Vector2(dx, dy)

            distance, collision_point = self._cast_single_ray(agent_pos, dir_vec)

            distances.append(distance/MAX_SENSOR_DIST) # normalized distance
            collision_points.append(collision_point)

        return distances, collision_points


    def _cast_single_ray(self, agent_pos, dir_vec):
        for distance in range(0, MAX_SENSOR_DIST, RAY_STEP):
            point = pygame.Vector2(
                int(agent_pos.x + dir_vec.x * distance),
                int(agent_pos.y + dir_vec.y * distance)
            )
            
            # check if out of bounds
            if point.x < 0 or point.x >= WORLD_WIDTH or point.y < 0 or point.y >= WORLD_HEIGHT:
                return distance, point
            
            # check for collision with segment in cell
            if self._point_collision(point):
                return distance, point
            
        # no collision found
        end_point = pygame.Vector2(
            int(agent_pos.x + dir_vec.x * MAX_SENSOR_DIST),
            int(agent_pos.y + dir_vec.y * MAX_SENSOR_DIST)
        )
        return MAX_SENSOR_DIST, end_point
            
            
    def _point_collision(self, point):
        grid_x = point.x // GRID_SIZE
        grid_y = point.y // GRID_SIZE
        cell_key = (grid_x, grid_y)

        if cell_key in self.grid: # check if any segments are in same cell as point
            # check each segment for collision
            for seg_idx in self.grid[cell_key]:
                segment = self.track_segments[seg_idx]
                offset_x = point.x - segment["rect"].x
                offset_y = point.y - segment["rect"].y

                try:
                    if segment["mask"].get_at((offset_x, offset_y)):
                        return True
                except:
                    continue
        return False



    def draw(self, screen:pygame.Surface, font, pop, camera_offset):
        # Draw the track
        screen_rect = pygame.Rect(camera_offset.x, camera_offset.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        for segment in self.track_segments:
            if segment["rect"].colliderect(screen_rect): # check if segment is in view
                offset_rect = segment["rect"].move(-camera_offset.x, -camera_offset.y)
                screen.blit(segment["surface"], offset_rect)
        
        # display text
        best_agent = pop.best_agents[0]
        generation_text = font.render(f"Generation: {pop.generation}", True, TEXT_COLOR)
        turn_text = font.render(f"Turn Rate (degrees/frame): {best_agent.angular_velocity: .2f}", True, TEXT_COLOR)
        speed_text = font.render(f"Speed (pixels/frame): {best_agent.speed: .2f}", True, TEXT_COLOR)
        fitness_text = font.render(f"Fitness: {best_agent.fitness: .2f}", True, TEXT_COLOR)

        screen.blit(generation_text, (10, 10))
        screen.blit(turn_text, (10, 30))
        screen.blit(speed_text, (10, 50))
        screen.blit(fitness_text, (10, 70))