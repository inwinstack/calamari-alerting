#!/usr/bin/env python

from setuptools import setup
import sys

if sys.version_info <= (2, 5):
    error = "ERROR: calamari-alert requires Python Version 2.6 or above...exiting."
    print(error)
    sys.exit(1)

requirements = [
    'pbr>=1.6',
    'six>=1.9.0',
    'stevedore>=1.5.0',
    'netaddr!=0.7.16,>=0.7.12',
    'requests!=2.8.0,>=2.5.2',
    'SQLAlchemy<1.1.0,>=0.9.9',
    'sqlalchemy_utils>=0.31.3',
    'simplejson>=2.2.0',
    'oslo.config>=2.7.0',
    'lxml>=3.5.0',
    'MySQL-python>=1.2.5',
    'psycopg2>=2.6.1'
]

setup(
    name='calamari-alert',
    version='0.1.0',
    description='Calamari Alert Service',
    author='Kyle Bai',
    author_email='kyle.b@inwinstack.com',
    url='http://www.inwinstack.com/',
    install_requires=requirements,
    packages=['calamari_alert', 'calamari_alert.tests', 'calamari_alert.api',
              'calamari_alert.common', 'calamari_alert.db'],
    license="MIT",
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Topic :: Internet",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 2.6",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.3",
                 "Programming Language :: Python :: 3.4"]
)