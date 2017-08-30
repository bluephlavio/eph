from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import os

import eph
from eph.config import get_config_files, create_config_file

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()


def install_config():
    config_file = get_config_files()[0]
    if not os.path.isfile(config_file):
        create_config_file(config_file)


class CustomInstall(install):

    def run(self):
        install_config()
        install.run(self)


class CustomDevelop(develop):

    def run(self):
        install_config()
        develop.run(self)


setup(
    name=eph.__project__,
    version=eph.__release__,
    description=eph.__description__,
    long_description=long_description,
    keywords=' '.join(eph.__keywords__),
    author=eph.__author__,
    author_email=eph.__author_email__,
    license=eph.__license__,
    url=eph.__url__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    install_requires=[
        'requests',
        'astropy',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': ['eph=eph.__main__:main'],
    },
    cmdclass={
        'develop': CustomDevelop,
        'install': CustomInstall,
    },
)
