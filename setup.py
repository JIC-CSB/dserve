from setuptools import setup

setup(
    name='dserve',
    packages=['dserve'],
    include_package_data=True,
    install_requires=[
        'dtoolcore>=0.15.0',
        'flask',
        'flask_cors',
    ],
)
