from setuptools import setup

version = "0.1.0"
url = "https://github.com/JIC-CSB/dserve"
readme = open('README.rst').read()

setup(
    name='dserve',
    packages=['dserve'],
    version=version,
    description="Tool to serve a dataset over HTTP",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    url=url,
    download_url="{}/tarball/{}".format(url, version),
    install_requires=[
        'dtoolcore>=0.15.0',
        'flask',
        'flask_cors',
    ],
    entry_points={
        'console_scripts': ['dserve=dserve.cli:main']
    },
    license="MIT")
