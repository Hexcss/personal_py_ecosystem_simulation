from multiprocessing import Process, Queue
from utils.generators.terrain import generate_terrain
from utils.generators.clouds import generate_clouds

class WorldInitializer:
    def __init__(self, config, noise_generator, loading_screen):
        self.config = config
        self.noise_generator = noise_generator
        self.loading_screen = loading_screen

    def initialize_world(self):
        queue = Queue()
        terrain_process = Process(target=generate_terrain, args=(queue, self.config, self.noise_generator))
        cloud_process = Process(target=generate_clouds, args=(queue, self.config, self.noise_generator))
        terrain_process.start()
        cloud_process.start()

        world_data, cloud_map = self.loading_screen.display(queue)

        terrain_process.join()
        cloud_process.join()

        return world_data, cloud_map
