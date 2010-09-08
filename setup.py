'''
Created on Sep 8, 2010

@author: Chris Glass (chirstopher.glass@divio.ch)
'''

import os
import sudsmagellan
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="sudsmagellan",
    version=sudsmagellan.__version__,
    description="A webservice cartographer using SUDS",
    author="Chris Glass",
    author_email="christopher.glass@divio.ch",
    maintainer="Chris Glass",
    maintainer_email="christopher.glass@divio.ch",
    packages=find_packages(exclude=['tests']),
    license= "GPL2",
    long_description=read('README'),
    install_requires=['python-ntlm', 'suds', 'optparse'],
    url="",
)
