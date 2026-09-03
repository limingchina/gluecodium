

"""Build script for the 'generated' Python extension module (pybind11)."""

from glob import glob

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        "generated",
        sorted(glob("pybind11/*.cpp")),
    ),
]

setup(
    name="generated",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
