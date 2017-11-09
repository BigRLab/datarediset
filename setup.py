from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
setup(
    name='datarediset',
    version='0.0.1',
    description='python\'s dict based on Redis',
    long_description='pudo\'s dataset on redis',
    url='https://github.com/RcrdBrt/datarediset',
    license='GPLv3',
    author='Riccardo Berto',
    author_email='riccardobrt@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    keywords='dataset dict redis',
    install_requires=['redis'],
)
