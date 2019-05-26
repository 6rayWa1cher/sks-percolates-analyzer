from setuptools import setup, find_namespace_packages

setup(
    name='sks.percolatesanalyzer',
    packages=find_namespace_packages(where='src') + ["tests"],
    package_dir={'': 'src', 'tests': 'tests'},
)
