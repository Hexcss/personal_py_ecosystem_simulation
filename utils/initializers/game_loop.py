import pygame
import random
import multiprocessing
from utils.entities.entity_spawner import EntitySpawner
from utils.functions.functions import calculate_path_for_entity

class GameLoop:
    def __init__(self, screen, config, input_handler, world_surface_handler, camera_handler, weather_handler, cloud_manager, cloud_map, world_data):
        self.screen = screen
        self.config = config
        self.input_handler = input_handler
        self.world_surface_handler = world_surface_handler
        self.camera_handler = camera_handler
        self.weather_handler = weather_handler
        self.cloud_manager = cloud_manager
        self.cloud_map = cloud_map
        self.world_data = world_data
        self.spawn_timer = 0
        self.max_entities = 20
        self.spawn_message = None
        self.spawn_message_timer = 0
        self.entity_spawner = EntitySpawner(self.world_data, self.config)
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        font = pygame.font.Font('./resources/fonts/font.ttf', 18)

        self.world_surface_handler.draw_world_to_surface(self.world_data)

        while self.running:
            dt = clock.tick(60) / 1000.0 
            self.handle_events()

            self.update_camera_and_fill_screen()

            self.draw_camera_coordinates(font)
            self.manage_and_draw_entities(dt, font)

            self.manage_clouds()
            
            pygame.display.flip()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.input_handler.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    self.select_entity(pygame.mouse.get_pos())
                elif event.button == 3: 
                    self.deselect_entity()
            if self.input_handler.redraw_world:
                self.world_surface_handler.draw_world_to_surface(self.world_data)
                self.input_handler.redraw_world = False
                
    def select_entity(self, mouse_pos):
        for entity in self.entity_spawner.entities:
            entity_rect = pygame.Rect(
                (entity.x - self.camera_handler.camera_x) * self.config["TILE_SIZE"],
                (entity.y - self.camera_handler.camera_y) * self.config["TILE_SIZE"],
                self.config["TILE_SIZE"],
                self.config["TILE_SIZE"]
            )
            if entity_rect.collidepoint(mouse_pos):
                entity.selected = True
                entity.play_sound_effect()
                break

    def deselect_entity(self):
        for entity in self.entity_spawner.entities:
            entity.selected = False     

    def manage_clouds(self):
        self.cloud_manager.update_cloud_position()
        visible_clouds = self.cloud_manager.get_visible_clouds(self.cloud_map)
        self.weather_handler.draw_weather(self.screen, visible_clouds)

    def update_camera_and_fill_screen(self):
        self.camera_handler.update_position()
        self.screen.fill((0, 0, 0))
        self.world_surface_handler.blit_world(self.screen, self.camera_handler.camera_x, self.camera_handler.camera_y)

    def draw_camera_coordinates(self, font):
        camera_coords_msg = f"Camera: ({self.camera_handler.camera_x}, {self.camera_handler.camera_y})"
        camera_coords_surface = font.render(camera_coords_msg, True, (255, 255, 255))
        coords_x = self.screen.get_width() - camera_coords_surface.get_width() - 10
        coords_y = 10
        self.screen.blit(camera_coords_surface, (coords_x, coords_y))

    def manage_and_draw_entities(self, dt, font):
        self.spawn_timer += dt
        if self.spawn_timer >= 10 and len(self.entity_spawner.entities) < self.max_entities:
            entity_type = random.choice(['sheep', 'pig', 'cow'])
            spawned_entity = self.entity_spawner.spawn_entity(entity_type)
            self.spawn_timer = 0
            self.spawn_message = f"{entity_type.capitalize()} spawned at ({spawned_entity.x}, {spawned_entity.y})"
            self.spawn_message_timer = 0

        if self.spawn_message:
            self.spawn_message_timer += dt
            if self.spawn_message_timer > 3:
                self.spawn_message = None
            message_surface = font.render(self.spawn_message, True, (255, 255, 255))
            self.screen.blit(message_surface, (10, 10))

        for entity in self.entity_spawner.entities:
            entity.move(self.world_data, self.config, self.entity_spawner.entity_positions)
            self.draw_entity(entity)
            self.draw_entity_health_bar(entity)

    def draw_entity(self, entity):
        entity_rect = pygame.Rect(
            (entity.x - self.camera_handler.camera_x) * self.config["TILE_SIZE"],
            (entity.y - self.camera_handler.camera_y) * self.config["TILE_SIZE"],
            self.config["TILE_SIZE"],
            self.config["TILE_SIZE"]
        )
        pygame.draw.rect(self.screen, entity.color, entity_rect)
        
        if entity.selected:
            self.draw_selected_entity_overlay(entity)
            if entity.target:
                self.draw_entity_path(entity)
                
    def draw_selected_entity_overlay(self, entity):
        radius_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        circle_x = (entity.x - self.camera_handler.camera_x) * self.config["TILE_SIZE"]
        circle_y = (entity.y - self.camera_handler.camera_y) * self.config["TILE_SIZE"]
        pygame.draw.circle(radius_surface, (255, 255, 255, 100), (int(circle_x), int(circle_y)), entity.view_radius * self.config["TILE_SIZE"])
        self.screen.blit(radius_surface, (0, 0))
        
    def draw_entity_path(self, entity):
        start_x = (entity.x - self.camera_handler.camera_x) * self.config["TILE_SIZE"]
        start_y = (entity.y - self.camera_handler.camera_y) * self.config["TILE_SIZE"]

        end_x = (entity.target[0] - self.camera_handler.camera_x) * self.config["TILE_SIZE"]
        end_y = (entity.target[1] - self.camera_handler.camera_y) * self.config["TILE_SIZE"]

        pygame.draw.line(self.screen, (255, 0, 0), (start_x, start_y), (end_x, end_y), 2)

        pygame.draw.circle(self.screen, (255, 223, 0), (int(end_x), int(end_y)), 5)


    def draw_entity_health_bar(self, entity):
        health_bar_width = (self.config["TILE_SIZE"] * 2) * (entity.hp / 100)
        health_bar_rect = pygame.Rect(
            (entity.x - self.camera_handler.camera_x) * self.config["TILE_SIZE"],
            (entity.y - self.camera_handler.camera_y) * self.config["TILE_SIZE"] - 10,
            health_bar_width,
            5
        )
        pygame.draw.rect(self.screen, (0, 255, 0), health_bar_rect)

        
