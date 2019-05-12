#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='ep2_tool',
    description='Tool to manage EP2 student attendance, formerly pk-tool',
    version='0.0.1',
    author='Felix Resch',
    author_email='felix.resch@tuwien.ac.at',
    packages=['ep2_tutors', 'src', 'ui', 'dialog'],
    install_requires=[
        'python-gitlab',
        'click',
        'gitpython',
        'six',
        'unicodecsv',
        'enum34',
        'cheetah3',
        'pyqt5'
    ]
)