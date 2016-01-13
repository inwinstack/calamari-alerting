from setuptools import setup, find_packages
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
    version='0.1.1',
    packages=find_packages(),
    description='Calamari Alert Service',
    author='Kyle Bai',
    author_email='kyle.b@inwinstack.com',
    url='http://www.inwinstack.com/',
    install_requires=requirements,
    license="MIT",
    entry_points={
        'console_scripts': [
            'calamari-alert = calamari_alert.run:main',
        ],
    },
)