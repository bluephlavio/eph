from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from shutil import copy2
import os
try:
    import configparser as configparser
except ImportError:
    import ConfigParser as configparser

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

parser = configparser.ConfigParser()
parser.read('setup.cfg')
meta = dict(parser.items('metadata'))


def install_config():
    try:
        dst = os.path.abspath(os.path.expanduser('~/.ephrc'))
        if not os.path.isfile(dst):
            src = os.path.abspath(os.path.join(here, 'eph/eph.cfg'))
            copy2(src, dst)
    except:
        pass


class CustomInstall(install):
    def run(self):
        install_config()
        install.run(self)


class CustomDevelop(develop):
    def run(self):
        install_config()
        develop.run(self)


setup(
    name=meta['package'],
    version=meta['release'],
    description=meta['description'],
    long_description=long_description,
    author=meta['author'],
    author_email=meta['author_email'],
    license=meta['license'],
    url=meta['url'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    install_requires=[
        'six>=1.0,<2.0',
        'requests>=2.0,<3.0',
        'astropy>=2.0,<4.0',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'eph=eph.cli:main',
        ],
    },
    cmdclass={
        'develop': CustomDevelop,
        'install': CustomInstall,
    },
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    python_requires='>=3.5'
)
