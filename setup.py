import os
import sys
import platform

from setuptools import setup, find_packages

setup(
    name='Recipes',
    version='0.1',
    description='',
    author='Mike Verdone',
    author_email='mike.verdone@gmail.com',
    url='',
    zip_safe=False,
    install_requires=[], #open('requirements.txt').read(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    entry_points={},
    )
