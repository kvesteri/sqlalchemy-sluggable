"""
SQLAlchemy-Sluggable
--------------------

Configurable slugs to SQLAlchemy models.
"""

from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)

setup(
    name='SQLAlchemy-Sluggable',
    version='0.1.1',
    url='https://github.com/kvesteri/sqlalchemy-sluggable',
    license='BSD',
    author='Janne Vanhala, Konsta Vesterinen',
    author_email='janne@fastmonkeys.com, konsta@fastmonkeys.com',
    description=(
        'Configurable slugs to SQLAlchemy models.'
    ),
    long_description=__doc__,
    packages=['sqlalchemy_sluggable'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'inflection==0.1.2',
        'SQLAlchemy==0.7.8',
    ],
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
