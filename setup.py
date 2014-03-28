from setuptools import setup, find_packages
import sys, os


setup(
    name='upasaporte',
    version='0.1',
    description="Libreria Python para verificar los datos entregados por U-Pasaporte",
    author='Francisco Madrid',
    author_email='fmadrid@dcc.uchile.cl',
    url='https://github.com/m4droid/U-Pasaporte',
    license='',
    packages=find_packages(
        exclude=[
            'ez_setup',
            'examples',
            'tests',
            'scripts'
        ]
    ),
    install_requires=[
        'pycrypto',
        'requests',
    ],
)
