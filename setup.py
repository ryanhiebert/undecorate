from os.path import dirname, join
from setuptools import setup


def fread(fn):
    return open(join(dirname(__file__), fn)).read()

setup(
    name='undecorate',
    version='0.2',
    description='Let your decorations be undone',
    long_description=fread('README.rst') + '\n\n' + fread('HISTORY.rst'),
    author='Ryan Hiebert',
    author_email='ryan@ryanhiebert.com',
    url='https://github.com/ryanhiebert/undecorate',
    license='MIT',
    py_modules=['undecorate'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: Developers',
    ]
)
