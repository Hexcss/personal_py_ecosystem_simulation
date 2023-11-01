import numpy as np
import random
import pygame

class Entity:
    def __init__(self, x, y, hp, color, sound_effect_path=None):
        self.x = x
        self.y = y
        self.hp = hp
        self.color = color
        self.target = None
        self.current_step = 0
        self.steps_to_target = 100
        self.view_radius = 25
        self.selected = False
        self.sound_effect = pygame.mixer.Sound(sound_effect_path) if sound_effect_path else None

    def move(self, world, config, entity_positions):
        if not self.target or self.current_step >= self.steps_to_target:
            self.select_new_target(world, config)
            self.current_step = 0

        if self.target:
            self.x = self.lerp(self.start_x, self.target[0], self.current_step / self.steps_to_target)
            self.y = self.lerp(self.start_y, self.target[1], self.current_step / self.steps_to_target)
            self.current_step += 1
        else:
            print("No path found!")

    def select_new_target(self, world, config):
        attempts = 0
        while True:
            dx = random.randint(-self.view_radius, self.view_radius)
            dy = random.randint(-self.view_radius, self.view_radius)
            target_x, target_y = self.x + dx, self.y + dy

            if (self.is_valid_location(target_x, target_y, world, config) and 
                self.is_unblocked_path(self.x, self.y, target_x, target_y, world, config)):
                self.start_x = self.x
                self.start_y = self.y
                self.target = (target_x, target_y)
                return
            attempts += 1
            if attempts > 100:  # safety measure to prevent infinite loop
                break

    def lerp(self, start, end, t):
        return start + t * (end - start)

    def is_valid_location(self, x, y, world, config):
        if 0 <= x < config["WIDTH"] and 0 <= y < config["HEIGHT"]:
            color = tuple(world[int(y), int(x)])
            return color in config["WALKABLE_TERRAINS"]
        return False
    
    def bresenham_line(self, x0, y0, x1, y1):
        """Generate points of a line using Bresenham's line algorithm."""
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        return points

    def is_unblocked_path(self, x0, y0, x1, y1, world, config):
        """Check if there's an unblocked path between two points."""
        for x, y in self.bresenham_line(x0, y0, x1, y1):
            if not self.is_valid_location(x, y, world, config):
                return False
        return True
    
    def play_sound_effect(self):
        if self.sound_effect:
            self.sound_effect.play()

class Sheep(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 100, (128, 128, 128), "./resources/sfx/sheep_sound.ogg") 

class Pig(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 80, (255, 192, 203), "./resources/sfx/pig_sound.ogg") 

class Cow(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 120, (139, 69, 19), "./resources/sfx/cow_sound.ogg") 
