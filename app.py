import pygame
from numpy.random import randint

from utils.noise.perlin_cython import PerlinNoiseGenerator
from utils.handlers.music import MusicHandler
from utils.handlers.camera import CameraHandler
from utils.handlers.input import InputHandler
from utils.handlers.world_surface import WorldSurfaceHandler
from utils.handlers.weather import WeatherHandler
from utils.initializers.world_initializer import WorldInitializer
from utils.initializers.game_loop import GameLoop
from utils.managers.clouds import CloudManager
from views.loading_screen import LoadingScreen
from config.config import CONFIG

class ProceduralWorld:
    def __init__(self, config, screen):
        self.screen = screen
        self.config = config
        self.noise_generator = PerlinNoiseGenerator(seed=randint(0, 1000))
        self.music_handler = MusicHandler(["atmosphere_1.mp3", "atmosphere_2.mp3", "atmosphere_3.mp3"])
        self.camera_handler = CameraHandler(config)
        self.input_handler = InputHandler(self.config, self.camera_handler, self.music_handler)
        self.loading_screen = LoadingScreen(screen, config)
        self.world_surface_handler = WorldSurfaceHandler(config)
        self.weather_handler = WeatherHandler(config, self.camera_handler)
        self.world_initializer = WorldInitializer(config, self.noise_generator, self.loading_screen)
        self.cloud_manager = CloudManager(config)
        self.world_data, self.cloud_map = self.world_initializer.initialize_world()
        
        self.game_loop = GameLoop(screen, config, self.input_handler, self.world_surface_handler, self.camera_handler, self.weather_handler, self.cloud_manager, self.cloud_map, self.world_data)
        
        self.music_handler.play_music()

    def run(self):
        self.game_loop.run()

def main():
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["SCREEN_WIDTH"], CONFIG["SCREEN_HEIGHT"]))
    pygame.display.set_caption("Procedural World with Perlin Noise")
    pygame.display.set_icon(pygame.image.load("./resources/assets/logo.png"))

    world = ProceduralWorld(CONFIG, screen)
    world.run()

    pygame.quit()

if __name__ == "__main__":
    main()
