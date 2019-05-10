"""
setup script
"""
from setuptools import setup,find_packages
import multigrids

config = {
    'description': 'Multigrids',
    'author': 'Rawser Spicer',
    'url': multigrids.__url__,
    'download_url': multigrids.__url__,
    'author_email': 'rwspicer@alaska.edu',
    'version': multigrids.__version__,
    'install_requires': ['numpy','pyyaml'],
    'packages': find_packages(),
    'scripts': [],
    'package_data': {},
    'name': 'Multigrids'
}

setup(**config)