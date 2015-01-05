# -*- coding: iso-8859-15 -*-
# =================================================================
#
# Copyright (c) 2014 Her Majesty the Queen in Right of Canada
#
# Author: Tom Kralidis <tom.kralidis@ec.gc.ca>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

from distutils.core import setup, Command
import os
import sys

import pygeometa

# set dependencies
INSTALL_REQUIRES = [line.strip() for line in open('requirements.txt')]

KEYWORDS = [
    'geospatial',
    'metadata',
    'catalogue',
    'discovery'
]

DESCRIPTION = '''
pygeometa is a Python package to generate metadata for meteorological datasets
'''

CONTACT = 'Meteorological Service of Canada, Environment Canada'

EMAIL = 'tom.kralidis@ec.gc.ca'

SCRIPTS = [
    os.path.join('bin', 'generate_metadata.py')
]

URL = 'http://gitlab.ssc.etg.gc.ca/ec-msc/pygeometa'


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        errno = subprocess.call([sys.executable, 'tests/run_tests.py'])
        raise SystemExit(errno)


# from https://wiki.python.org/moin/Distutils/Cookbook/AutoPackageDiscovery
def is_package(path):

    """decipher whether path is a Python package"""

    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )


def find_packages(path, base=''):
    """Find all packages in path"""

    packages = {}
    for item in os.listdir(path):
        dirpath = os.path.join(path, item)
        if is_package(dirpath):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dirpath
            packages.update(find_packages(dirpath, module_name))
    return packages


def find_packages_templates(location='.'):
    """get dirs to be specified as package_data keys (templates)"""

    packages = []
    for root, dirs, files in os.walk(location):
        if 'templates' in dirs:  # include as a package_data key
            print root, dirs, files
            packages.append(root.replace(os.sep, '.').replace('..', ''))

    return {'pygeometa': ['templates/*/*.j2']}
    return packages


setup(
    name='pygeometa',
    version=pygeometa.__version__,
    description=DESCRIPTION.strip(),
    long_description=open('README.md').read(),
    license='MIT',
    platforms='all',
    keywords=' '.join(KEYWORDS),
    author=CONTACT,
    author_email=EMAIL,
    maintainer=CONTACT,
    maintainer_email=EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages('.').keys(),
    package_data=find_packages_templates('pygeometa'),
    scripts=SCRIPTS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS'
    ],
    cmdclass={'test': PyTest},
    test_suite='tests.run_tests'
)
