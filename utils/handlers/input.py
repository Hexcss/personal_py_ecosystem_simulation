import pygame

class InputHandler:
    def __init__(self, config, camera_handler, music_handler):
        self.config = config
        self.camera_handler = camera_handler
        self.music_handler = music_handler
        self.redraw_world = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: 
                self.config["TILE_SIZE"] = min(32, self.config["TILE_SIZE"] + 2) 
                self.redraw_world = True
            if event.button == 5: 
                self.config["TILE_SIZE"] = max(4, self.config["TILE_SIZE"] - 2)
                self.redraw_world = True

        if event.type == pygame.USEREVENT:
            self.music_handler.play_random_track()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.camera_handler.target_y > 0:
            self.camera_handler.target_y -= 1
        if keys[pygame.K_s] and self.camera_handler.target_y < self.config["HEIGHT"] - self.config["SCREEN_HEIGHT"] // self.config["TILE_SIZE"]:
            self.camera_handler.target_y += 1
        if keys[pygame.K_a] and self.camera_handler.target_x > 0:
            self.camera_handler.target_x -= 1
        if keys[pygame.K_d] and self.camera_handler.target_x < self.config["WIDTH"] - self.config["SCREEN_WIDTH"] // self.config["TILE_SIZE"]:
            self.camera_handler.target_x += 1

        return self.redraw_world