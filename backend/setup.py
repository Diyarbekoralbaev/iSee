from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name='diyar_func',
    version='1.0',
    packages=find_packages(),
    ext_modules=cythonize("cy_func.pyx"),
    install_requires=[
        'aiohttp',
        'Pillow',
        'google-generativeai',
    ],
)