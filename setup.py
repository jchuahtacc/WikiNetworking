from distutils.core import setup

setup(
    name='WikiNetworking',
    version='0.1',
    packages=['wikinetworking',],
    install_requires=[
    	"jupyter",
    	"networkx",
    	"matplotlib",
    	"mpld3",
    	"pyquery"
    ],
    license='MIT License',
    long_description='Utilities for crawling and text mining a wiki and representing links as a node graph',
)