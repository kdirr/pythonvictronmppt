'''
 # @ Author: Konstantin Dirr
 # @ Create Time: 2023-06-11
 '''

from setuptools import setup

setup(
    name = "pythonvictronmppt",
    version = "0.0.2",
    author = "Konstantin Dirr",
    author_email = "k.dirr@beo-software.de",
    description = ("Minimal python class for parsing statistics data from Victron devices using VE.Direct protocol via serial port."),
    license = "GPLv3",
    keywords = "vedirect victron mppt",
    #url = "http://packages.python.org/an_example_pypi_project",
    packages = ['pythonvictronmppt'],
    #long_description=read('README'),
    install_requires=['pyserial'],
    python_requires='>=3',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Console"
    ],
)