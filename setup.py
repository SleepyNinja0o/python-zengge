#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
import sys
import warnings

dynamic_requires = []

version = 0.3

setup(
    name='zengge',
    version=0.3,
    author='Austin Parsons',
    author_email='vb6email@gmail.com',
    url='https://github.com/SleepyNinja0o/python-zengge',
    packages=find_packages(),
    scripts=[],
    description='Python API for controlling Zengge LED bulbs',
    classifiers=[
        'Development Status :: 5 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    zip_safe=False,
)
