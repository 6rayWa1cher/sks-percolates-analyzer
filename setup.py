from setuptools import setup, find_namespace_packages

setup(
    name='sks.percolatesanalyzer',
    version='1.0.0',
    packages=find_namespace_packages(where='src') + ["tests"],
    package_dir={'': 'src', 'tests': 'tests'},
    license='MIT License',
    url='https://github.com/6rayWa1cher/sks-percolates-analyzer',
    author='6rayWa1cher and Alstrasz',
    author_email='info@a6raywa1cher.com',
    description='Percolates analyzer with Monte-Carlo magic',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
