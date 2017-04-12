from setuptools import setup

setup(
    name='dserve',
    packages=['dserve'],
    include_package_data=True,
    install_requires=[
        'dtoolcore',
        'flask',
        'flask_cors',
    ],
)
