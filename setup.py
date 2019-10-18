#!/usr/bin/env python

from setuptools import setup

setup(
    # GETTING-STARTED: set your app name:
    name='Proxable-Utilities',
    # GETTING-STARTED: set your app version:
    version='1.0',
    # GETTING-STARTED: set your app description:
    description='Proxable Utilities Package',
    # GETTING-STARTED: set author name (your name):
    author='Dylan Turnbull',
    # GETTING-STARTED: set author email (your email):
    author_email='dturnbu@transunion.com',
    # GETTING-STARTED: set author url (your url):
    url='http://www.python.org/sigs/distutils-sig/',
    # Name of the module:
    packages=['ProxableUtils'],
    # GETTING-STARTED: define required django version:
    install_requires=[
        'influxdb==4.1.1',
        'six==1.10.0',
        'configparser==3.5.0',
        'requests==2.20.0',
        'urllib3==1.21.1'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/requests/',
        'https://pypi.python.org/simple/six/',
        'https://pypi.python.org/simple/influxdb/',
        'https://pypi.python.org/simple/configparser/'
    ],
)