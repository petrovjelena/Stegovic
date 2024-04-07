import setuptools
from distutils import setup


setup(
    name='stegovic',
    version='1.0.0',
    author='You',
    packages=['stegovic'],
    entry_points={
        'console_scripts': ['stegovic=stegovic.entry:stegovic_entry_point'],
    },
)