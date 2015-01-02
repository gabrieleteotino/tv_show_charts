"""
Created on 24/dic/2014

@author: Gabriele Teotino
"""

from setuptools import setup

setup(
    name='tv_show_charts',
    version='0.1',
    description='TV Shows Charting imports all the TV series from IMDb and create charts',
    url='https://github.com/gabrieleteotino/tv_show_charts',
    author='Gabriele Teotino',
    author_email='ibt.org@gmail.com',
    license='MIT',
    packages=['tv_show_charts'],
    install_requires = ['matplotlib>=1.4.2'],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['tv_show_charts=tv_show_charts.command_line:main'],
    }
)