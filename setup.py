"""
gaema
=====
gaema is a library that provides various authentication systems for Google App
Engine. It is basically the tornado.auth module extracted to work on App Engine
and independently of any framework.

It supports login using:

- OpenId
- OAuth
- Google Accounts
- Facebook
- FriendFeed
- Twitter

You can use one, all or a mix of these auth methods. This is done with minimal
overhead: gaema is small and doesn't have any dependencies, thanks to the
awesome work done by the Tornado crew.

gaema only authenticates an user, and doesn't provide persistence such as
sessions or secure cookies to keep the user logged in. Because each framework
do these things in a different way, it is up to the framework to implement
these mechanisms.
"""
from setuptools import setup, find_packages


setup(
    name='gaema',
    version='0.1',
    url='http://code.google.com/p/gaema/',
    license='Apache Software License',
    author='Rodrigo Moraes',
    author_email='rodrigo.moraes@gmail.com',
    description='tornado.auth tweaked to work on Google App Engine',
    long_description=__doc__,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['gaema']
)
