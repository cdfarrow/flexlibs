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
    packages=find_packages(exclude=('tests', 'docs'))
)
