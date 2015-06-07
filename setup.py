import sys

from setuptools import find_packages, setup

backports = []
if sys.version_info < (3, 4):
    backports.append('enum34')

config = {
    'name': 'alchemy',
    'description': 'Potion-crafting game',
    'version': '0.1',
    'author': 'eltoraz',
    'author_email': 'eltoraz@outlook.com'
    'url': 'https://github.com/eltoraz/alchemy',
    'packages': find_packages(),
    'install_requires': backports + ['nose']
}

setup(**config)
