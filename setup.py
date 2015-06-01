from setuptools import find_packages, setup

config = {
    'name': 'alchemy',
    'description': 'Potion-crafting game',
    'version': '0.1',
    'author': 'eltoraz',
    'author_email': 'eltoraz@outlook.com'
    'url': 'https://github.com/eltoraz/alchemy',
    'packages': find_packages(),
    'install_requires': ['nose']
}

setup(**config)
