from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "perlin_cython",  # Change this to "noise.perlin_cython" if you want it inside the `noise` directory
        sources=["perlin_cython.pyx"],
    )
]

setup(
    ext_modules=cythonize(extensions),
    include_dirs=[np.get_include()]
)
