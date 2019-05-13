from setuptools import setup, find_namespace_packages

setup(
    name='sks.percolates_analyzer',
    packages=find_namespace_packages(where='src') + ["tests"],
    package_dir={'': 'src', 'tests': 'tests'},
)
