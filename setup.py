from setuptools import find_packages, setup

setup(
    name='wholang',
    packages=find_packages(include=['wholang']),
    version='0.1.0',
    description="A Python library for Sherman's Circular",
    author='Impronoucabl',
    license='MIT',
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    test_suite='tests'
)