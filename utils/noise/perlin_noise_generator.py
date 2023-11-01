import numpy as np

class PerlinNoiseGenerator:
    
    def __init__(self, seed=42):
        np.random.seed(seed)

    @staticmethod
    def generate_gradient_vectors(grid_width, grid_height):
        angles = 2 * np.pi * np.random.rand(grid_width, grid_height)
        gradients = np.dstack((np.cos(angles), np.sin(angles)))
        return gradients

    @staticmethod
    def dot_grid_gradient(ix, iy, x, y, gradients):
        dx = x - ix
        dy = y - iy
        gradient = gradients[min(iy, gradients.shape[0]-1), min(ix, gradients.shape[1]-1)]
        return gradient[0] * dx + gradient[1] * dy

    @staticmethod
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def interpolate(a0, a1, w):
        return a0 + PerlinNoiseGenerator.fade(w) * (a1 - a0)

    def perlin_noise(self, width, height, grid_width, grid_height):
        gradients = self.generate_gradient_vectors(grid_width, grid_height)
        values = np.empty((width, height))

        for y in range(height):
            for x in range(width):
                x_grid = min(x * (grid_width - 1) / (width - 1), grid_width - 2)
                y_grid = min(y * (grid_height - 1) / (height - 1), grid_height - 2)

                x0 = int(x_grid)
                x1 = (x0 + 1) % grid_width
                y0 = int(y_grid)
                y1 = (y0 + 1) % grid_height

                n00 = self.dot_grid_gradient(x0, y0, x_grid, y_grid, gradients)
                n10 = self.dot_grid_gradient(x1, y0, x_grid, y_grid, gradients)
                n01 = self.dot_grid_gradient(x0, y1, x_grid, y_grid, gradients)
                n11 = self.dot_grid_gradient(x1, y1, x_grid, y_grid, gradients)

                wx = x_grid - x0
                wy = y_grid - y0

                ix0 = self.interpolate(n00, n10, wx)
                ix1 = self.interpolate(n01, n11, wx)

                values[y, x] = self.interpolate(ix0, ix1, wy)

        return values

    def perlin_noise_octaves(self, width, height, grid_width, grid_height, octaves, persistence):
        total_amplitude = 0
        amplitude = 1.0
        frequency = 1.0
        noise = np.zeros((width, height))

        for i in range(octaves):
            noise += amplitude * self.perlin_noise(width, height, int(grid_width * frequency), int(grid_height * frequency))
            total_amplitude += amplitude
            amplitude *= persistence
            frequency *= 2

        return noise / total_amplitude
