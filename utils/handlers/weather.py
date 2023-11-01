import pygame

class WeatherHandler:
    def __init__(self, config, camera_handler):
      self.config = config
      self.camera_handler = camera_handler

    def draw_weather(self, screen, cloud_map):
      start_y = int(self.camera_handler.camera_y)
      start_x = int(self.camera_handler.camera_x)
      end_y = min(self.config["HEIGHT"], start_y + self.config["SCREEN_HEIGHT"] // self.config["TILE_SIZE"])
      end_x = min(self.config["WIDTH"], start_x + self.config["SCREEN_WIDTH"] // self.config["TILE_SIZE"])

      for y in range(start_y, end_y):  
            for x in range(start_x, end_x):  
              cloud_intensity = cloud_map[y, x]
              
              if cloud_intensity > 0.6:
                  pygame.draw.circle(screen, self.config["COLORS"]["CLOUD"], ((x - int(self.camera_handler.camera_x)) * self.config["TILE_SIZE"] + self.config["TILE_SIZE"]//2, (y - int(self.camera_handler.camera_y)) * self.config["TILE_SIZE"] + self.config["TILE_SIZE"]//2), int(self.config["TILE_SIZE"] * cloud_intensity), 1)
