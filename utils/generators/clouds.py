def generate_clouds(queue, config, noise_generator):
    large_cloud_map = noise_generator.perlin_noise_octaves(config["WIDTH"] * 2, config["HEIGHT"] * 2, 8, 8, octaves=2, persistence=0.3)
    large_cloud_map = (large_cloud_map - large_cloud_map.min()) / (large_cloud_map.max() - large_cloud_map.min())
    queue.put(('clouds', large_cloud_map))
