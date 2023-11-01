class CameraHandler:
    def __init__(self, config):
        self.config = config
        self.camera_x, self.camera_y = 0, 0
        self.target_x, self.target_y = self.camera_x, self.camera_y 
        self.speed = config["CAMERA_SPEED"]

    def update_position(self):
        tile_size = self.config["TILE_SIZE"]
        max_camera_x = (self.config["WIDTH"] * tile_size - self.config["SCREEN_WIDTH"]) // tile_size
        max_camera_y = (self.config["HEIGHT"] * tile_size - self.config["SCREEN_HEIGHT"]) // tile_size

        self.camera_x += (self.target_x - self.camera_x) * self.speed
        self.camera_y += (self.target_y - self.camera_y) * self.speed

        # Ensuring camera boundaries
        self.camera_x = max(0, min(self.camera_x, max_camera_x))
        self.camera_y = max(0, min(self.camera_y, max_camera_y))