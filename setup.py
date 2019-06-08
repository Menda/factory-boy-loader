# -*- coding: utf-8 -*-
import os
from os.path import join, abspath
from setuptools import setup

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(join(abspath(__file__), os.pardir)))

setup(
    name='factory-boy-loader',
    version='0.0.1',
    url='https://github.com/Menda/factory-boy-loader',
    description=(
        'Tool that helps to load factories created with factory_boy '
        'the same way data fixtures are loaded in Django.'
    ),
    author='Rafael Muñoz Cárdenas',
    author_email='contact@rmunoz.net',
    packages=[
        'factory_loader',
    ],
    provides=[
        'factory_loader'
    ],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=[
        'factory_boy',
        'factory',
        'fixtures',
        'initialdata',
        'load_initial_data',
        'loadinitialdata',
    ],
)
