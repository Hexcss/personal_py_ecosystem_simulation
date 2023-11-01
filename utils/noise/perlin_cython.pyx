import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cdef class PerlinNoiseGenerator:
    def __init__(self, int seed=42):
        np.random.seed(seed)

    @staticmethod
    cdef np.ndarray generate_gradient_vectors(int grid_width, int grid_height):
        cdef np.ndarray angles = 2 * np.pi * np.random.rand(grid_width, grid_height)
        cdef np.ndarray gradients = np.dstack((np.cos(angles), np.sin(angles)))
        return gradients

    @staticmethod
    cdef float dot_grid_gradient(int ix, int iy, float x, float y, np.ndarray gradients):
        cdef float dx = x - ix
        cdef float dy = y - iy
        cdef float[2] gradient = gradients[min(iy, gradients.shape[0]-1), min(ix, gradients.shape[1]-1)]
        return gradient[0] * dx + gradient[1] * dy

    @staticmethod
    cdef float fade(float t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    cdef float interpolate(float a0, float a1, float w):
        return a0 + PerlinNoiseGenerator.fade(w) * (a1 - a0)

    def perlin_noise(self, int width, int height, int grid_width, int grid_height):
        cdef np.ndarray gradients = PerlinNoiseGenerator.generate_gradient_vectors(grid_width, grid_height)
        cdef np.ndarray values = np.empty((width, height), dtype=np.float32)
        cdef float x_grid, y_grid
        cdef int x0, x1, y0, y1
        cdef float n00, n10, n01, n11, wx, wy, ix0, ix1

        for y in range(height):
            for x in range(width):
                x_grid = min(x * (grid_width - 1) / (width - 1), grid_width - 2)
                y_grid = min(y * (grid_height - 1) / (height - 1), grid_height - 2)

                x0 = int(x_grid)
                x1 = (x0 + 1) % grid_width
                y0 = int(y_grid)
                y1 = (y0 + 1) % grid_height

                n00 = PerlinNoiseGenerator.dot_grid_gradient(x0, y0, x_grid, y_grid, gradients)
                n10 = PerlinNoiseGenerator.dot_grid_gradient(x1, y0, x_grid, y_grid, gradients)
                n01 = PerlinNoiseGenerator.dot_grid_gradient(x0, y1, x_grid, y_grid, gradients)
                n11 = PerlinNoiseGenerator.dot_grid_gradient(x1, y1, x_grid, y_grid, gradients)

                wx = x_grid - x0
                wy = y_grid - y0

                ix0 = PerlinNoiseGenerator.interpolate(n00, n10, wx)
                ix1 = PerlinNoiseGenerator.interpolate(n01, n11, wx)

                values[y, x] = PerlinNoiseGenerator.interpolate(ix0, ix1, wy)

        return values

    def perlin_noise_octaves(self, int width, int height, int grid_width, int grid_height, int octaves, float persistence):
        cdef float total_amplitude = 0
        cdef float amplitude = 1.0
        cdef float frequency = 1.0
        cdef np.ndarray noise = np.zeros((width, height), dtype=np.float32)

        for i in range(octaves):
            noise += amplitude * self.perlin_noise(width, height, int(grid_width * frequency), int(grid_height * frequency))
            total_amplitude += amplitude
            amplitude *= persistence
            frequency *= 2

        return noise / total_amplitude
