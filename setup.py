"""Setup script"""
from setuptools import setup, find_packages
setup(
    name="htlprettify",
    version="0.1",
    packages=find_packages(exclude=(
        'tmp', 'build', 'dist', 'htlprettify.egg-info' 'tests', 'docs')),
    entry_points={
        'console_scripts': [
            'htlprettify = htlprettify.main:main',
        ],
    },
    include_package_data=True
)
