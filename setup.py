#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='django-database-files-ny',
    version='0.2.2',
    packages=find_packages(),
    description='A storage system for Django that stores uploaded files in the database.',
    author='Sam Spencer',
    author_email='sam@aristotlemetadata.com',
    url='http://github.com/legostormtroopr/django-database-files/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
    ]
)
