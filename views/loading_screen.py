import pygame
import time
from utils.handlers.music import MusicHandler

class LoadingScreen:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.music_handler = MusicHandler(["loading.mp3"])
        self.music_handler.play_music()
        
        # Use a pixel art styled font
        self.font = pygame.font.Font('./resources/fonts/font.ttf', 32)
        
        # Load the logo
        original_logo = pygame.image.load("./resources/assets/logo.png")
        self.logo = pygame.transform.scale(original_logo, (original_logo.get_width() // 8, original_logo.get_height() // 8))
        
        # Load and scale the background image
        original_background = pygame.image.load("./resources/assets/background.png")
        self.background = pygame.transform.scale(original_background, (self.config["SCREEN_WIDTH"], self.config["SCREEN_HEIGHT"]))
        
        self.progress = 0
        self.target_progress = 0  # New attribute for target progress
        self.current_task = 'Generating terrain'
        self.frames_elapsed = 0 

    def get_dots(self):
        dot_count = (self.frames_elapsed // 30) % 4 
        return '.' * dot_count

    def draw_loading_bar(self, position, width, height, progress):
        BORDER_COLOR = (240, 180, 50)  # A golden color to match the sunset
        FILL_COLOR = (90, 150, 60)  # A greenish color to match the trees
        pygame.draw.rect(self.screen, BORDER_COLOR, (position[0], position[1], width, height), 5)
        pygame.draw.rect(self.screen, FILL_COLOR, (position[0], position[1], width * progress, height))

    def display(self, queue):
        start_ticks = pygame.time.get_ticks()
        world_data = None
        cloud_data = None

        while world_data is None or cloud_data is None or self.progress < 1.0:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None, None 
            
            self.frames_elapsed += 1  # Increment the frame count

            # Smoothly interpolate the progress value
            self.progress += (self.target_progress - self.progress) * 0.05

            # Use the scaled and centered background image
            self.screen.blit(self.background, (0, 0))

            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0
            text_color = (255, 255, 255)  # Bright white for better visibility
            text_surface = self.font.render('{:.2f} seconds'.format(elapsed_time), True, text_color)
            text_rect = text_surface.get_rect(center=(self.config["SCREEN_WIDTH"] / 2, self.config["SCREEN_HEIGHT"] / 2 - 120))
            self.screen.blit(text_surface, text_rect)

            # Logo
            if self.logo:
                logo_rect = self.logo.get_rect(center=((self.config["SCREEN_WIDTH"] / 2), self.config["SCREEN_HEIGHT"] / 2 - 200))
                self.screen.blit(self.logo, logo_rect)

            # Loading bar
            self.draw_loading_bar((self.config["SCREEN_WIDTH"] / 2 - 150, self.config["SCREEN_HEIGHT"] / 2 + 80), 300, 30, self.progress)
            
            # Display current task with animated dots
            task_surface = self.font.render(self.current_task + self.get_dots(), True, text_color)
            task_rect = task_surface.get_rect(center=(self.config["SCREEN_WIDTH"] / 2, self.config["SCREEN_HEIGHT"] / 2 + 150))
            self.screen.blit(task_surface, task_rect)

            pygame.display.flip()

            while not queue.empty():
                task, data = queue.get()
                if task == 'terrain':
                    self.target_progress = 0.5
                    self.current_task = 'Generating clouds'
                    world_data = data
                elif task == 'clouds':
                    self.target_progress = 1.0
                    self.current_task = 'Starting up'
                    cloud_data = data

            if self.progress >= 0.995:  
                time.sleep(0.5) 

            if world_data is not None and cloud_data is not None and self.progress >= 0.995:
                self.music_handler.stop_music()
                break

        return world_data, cloud_data
