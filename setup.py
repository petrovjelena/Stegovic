from setuptools import setup, find_packages


setup(
    name='Stegovic',
    version='1.2',
    author='Jelena Petrovic',
    url='https://github.com/petrovjelena/Stegovic.git',
    packages=find_packages(),
    scripts=['install.sh'],
    install_requires=[
        "setuptools>=68.2.2",
        "pillow>=10.0.1",
    ],
)
