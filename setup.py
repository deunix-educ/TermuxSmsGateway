'''
Created on 30 mars 2021

@author: denis
'''
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name = 'smsquitto',
    version = '1.0',
    description = 'SMS gateway using an Android phone',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Deunix from e-educ',
    author_email = 'deunix@e-educ.fr',
    #url='https://github.com/pypa/termux-smsquitto',
    classifiers = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Any public',
        'Topic :: Software Development :: Sms Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords = 'Termux, sms, Android, notification, mqtt',

    package = ['smsquitto'],
    package_data = {'smsquitto': ['*.yaml'] },
    package_dir = {'smsquitto': './smsquitto' },
    packages=find_packages(where='.'),

    python_requires = '>=3.7',
    install_requires=['paho-mqtt', 'rsa', 'PyYAML', 'supervisor'],




)


