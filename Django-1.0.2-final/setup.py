longdesc = '''
Django 1.0.2.
See also: http://www.djangoproject.com/download/
'''

import ez_setup
ez_setup.use_setuptools()

import os, sys
try:
    from setuptools import setup
    kw = {
    }
    
except ImportError:
    from distutils.core import setup
    kw = {}
    
from setuptools import find_packages
_packages = [p for p in find_packages()]
setup(
    name = "Django",
    version = "1.0.2",
    packages = _packages,
    description = "Django 1.0.2 Distro",
    author = "www.djangoproject.com",
    url = "http://www.djangoproject.com/download/",
    download_url = 'http://www.djangoproject.com/download/',
    license = 'BSD license (http://code.djangoproject.com/file/django/trunk/LICENSE)',
    platforms = 'Posix; Windows',
    classifiers = [ 'Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: GPL (Restricted to Non-Commercial Educational Use Only).',
                    'Operating System :: OS Independent',
                    'Topic :: Internet' ],
    long_description = longdesc,
    **kw
)

