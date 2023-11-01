from utils.functions.functions import get_wrapped_slice

class CloudManager:
    def __init__(self, config):
        self.config = config
        self.cloud_x_offset = 0
        self.cloud_y_offset = 0

    def update_cloud_position(self):
        self.cloud_x_offset = (self.cloud_x_offset + self.config["CLOUD_SPEED"][0]) % (self.config["WIDTH"] * 2)
        self.cloud_y_offset = (self.cloud_y_offset + self.config["CLOUD_SPEED"][1]) % (self.config["HEIGHT"] * 2)

    def get_visible_clouds(self, cloud_map):
        return get_wrapped_slice(cloud_map, int(self.cloud_x_offset), int(self.cloud_x_offset + self.config["WIDTH"]), int(self.cloud_y_offset), int(self.cloud_y_offset + self.config["HEIGHT"]))
