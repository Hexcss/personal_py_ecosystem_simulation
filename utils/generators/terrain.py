import numpy as np

def generate_terrain(queue, config, noise_generator):
    noise = noise_generator.perlin_noise_octaves(config["WIDTH"], config["HEIGHT"], 8, 8, octaves=4, persistence=0.5)
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    world = np.empty((config["WIDTH"], config["HEIGHT"], 3), dtype=int)
    
    for y in range(config["HEIGHT"]):
          for x in range(config["WIDTH"]):
              value = noise[y, x]
              if value > 0.75:    
                  world[y, x] = config["COLORS"]["SNOW"]
              elif value > 0.6:     
                  world[y, x] = config["COLORS"]["MOUNTAIN"]
              elif value > 0.4:     
                  world[y, x] = config["COLORS"]["GRASS"]
              elif value > 0.35:    
                  world[y, x] = config["COLORS"]["SAND"]
              elif value > 0.2:      
                  world[y, x] = config["COLORS"]["WATER"]
              else:                  
                  world[y, x] = config["COLORS"]["DEEP_WATER"]
    
    queue.put(('terrain', world))