from distutils.core import setup

setup(
    name='WikiNetworking',
    version='0.1',
    packages=['wikinetworking',],
    description='Utilities for graphing Wiki articles',
    author='Joon-Yee Chuah',
    author_email='jchuah@tacc.utexas.edu',
    url='https://github.com/jchuahtacc/WikiNetworking',
    download_url='https://github.com/jchuahtacc/WikiNetworking/archive/0.1.tar.gz',
    keywords=['graphing', 'wiki', 'jupyter'],
    classifiers=[],
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
