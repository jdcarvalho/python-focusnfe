#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='python-focusnfe',
    version='1.0.0',
    description="Python FocusNFe API v2 Binding",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    author='Larysson Alves',
    author_email='larysson.alves@e-north.com.br',
    install_requires=[
        "requests>=2.18.0",
    ],
    url='https://github.com/devlarysson/python-focusnfe',
    packages=find_packages(),
)
