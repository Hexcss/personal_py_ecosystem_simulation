import pygame

class WorldSurfaceHandler:
    def __init__(self, config):
        self.config = config
        self.world_surface = pygame.Surface((self.config["WIDTH"] * self.config["TILE_SIZE"], self.config["HEIGHT"] * self.config["TILE_SIZE"]))

    def draw_world_to_surface(self, world):
        for y in range(self.config["HEIGHT"]):
            for x in range(self.config["WIDTH"]):
                color = world[y, x]
                pygame.draw.rect(self.world_surface, color, (x * self.config["TILE_SIZE"], y * self.config["TILE_SIZE"], self.config["TILE_SIZE"], self.config["TILE_SIZE"]))
        
    def blit_world(self, screen, camera_x, camera_y):
        screen.blit(self.world_surface, (-camera_x * self.config["TILE_SIZE"], -camera_y * self.config["TILE_SIZE"]))
        
