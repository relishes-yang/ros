from catkin_pkg.python_setup import generate_distutils_setup
from setuptools import setup

d = generate_distutils_setup(
    packages=['posvel_control'],
    package_dir={'': '.'},  # ✅ 关键：使用当前目录（.）
)
setup(**d)
