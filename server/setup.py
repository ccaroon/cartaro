from setuptools import setup
import cartaro.version

setup(
    name='cartaro',
    url='https://github.com/ccaroon/cartaro',
    maintainer='Craig N. Caroon',
    maintainer_email='craig@caroon.org',
    version=cartaro.version.VERSION,
    packages=[
        'cartaro',
        'cartaro.controller',
        'cartaro.controller.time_off',
        'cartaro.model', 'cartaro.model.time_off',
        'cartaro.utils'
    ],
    package_dir={'cartaro': 'cartaro'},
    install_requires=[
        "arrow ~= 1.2.2",
        "cryptography ~= 3.3.1",
        "flask ~= 2.0.0",
        "gunicorn ~= 20.1.0",
        "inflector ~= 3.0.1",
        "requests ~= 2.25.1",
        "tinydb ~= 4.3.0",
        "wheel ~= 0.37.1"
    ],
    scripts=['bin/cartaroctl']
)
