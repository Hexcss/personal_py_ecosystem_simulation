import random
from utils.entities.entities import Sheep, Pig, Cow

class EntitySpawner:
    def __init__(self, world, config):
        self.world = world
        self.config = config
        self.entities = []
        self.entity_positions = set()

    def spawn_entity(self, entity_type):
        x = random.randint(0, self.config["WIDTH"] - 1)
        y = random.randint(0, self.config["HEIGHT"] - 1)

        while not self.is_valid_spawn_location(x, y):
            x = random.randint(0, self.config["WIDTH"] - 1)
            y = random.randint(0, self.config["HEIGHT"] - 1)

        entity = None
        
        if entity_type == "sheep":
            entity = Sheep(x, y)
            self.entities.append(entity)
        elif entity_type == "pig":
            entity = Pig(x, y)
            self.entities.append(entity)
        elif entity_type == "cow":
            entity = Cow(x, y)
            self.entities.append(entity)
            
        self.entity_positions.add((entity.x, entity.y))    
        
        return entity

    def is_valid_spawn_location(self, x, y):
        color = self.world[y, x]
        return tuple(color) in [self.config["COLORS"]["GRASS"], self.config["COLORS"]["SAND"]]
