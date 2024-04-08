from setuptools import setup, find_packages


setup(
    name='Stegovic',
    version='1.0.0',
    author='Jelena Petrovic',
    url='https://github.com/petrovjelena/Stegovic.git',
    packages=find_packages(),
    scripts=['install.sh'],
    install_requires=[
        "setuptools>=44.1",
        "argparse>=1.4.0",
        "pillow>=9.0.0",
        "requests>=2.25.1",
    ],
)
