# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='flexlibs',
    version='2.0.0',
    description='Library for accessing FieldWorks Language Explorer projects',
    long_description=readme,
    author='Craig Farrow',
    author_email='flextoolshelp@gmail.com',
    url='https://github.com/cdfarrow/flexlibs',
    license=license,
    platforms=['Windows', 'Linux'],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'pythonnet>=2.0.0',
        'future;python_version=="2.7"',
        'sphinx'
        ],
    include_package_data=True
)
