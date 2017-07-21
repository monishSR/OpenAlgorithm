import os
from setuptools import setup
import sys

if sys.version_info < (3, 5):
	sys.exit('Sorry, Python < 3.5 is not supported')

os.system("sudo apt-get install python3-tk")

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "OpenAnalysis",
    version = "0.0.1",
    author = "OpenWeavers",
    author_email = "me.vinayakakv@gmail.com",
    description = ("An open source package to analyse and visualise algorithms and data structures"),
    license = "GNU",
    keywords = "OpenWeavers product",
    url = "http://openalgorithm.readthedocs.io",
    packages=['OpenAnalysis'],
    long_description=read('Readme.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU License",
    ],
    install_requires=[
	'scipy',
	'numpy',
	'matplotlib',
    ],
    extras_require={
	"extensions" : [
            'jupyter', 
            'ipython',
        ],
    }	
)
