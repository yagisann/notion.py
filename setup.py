from setuptools import setup

DESCRIPTION = 'notion.py: An api wrapper and data models for Notion API.'
NAME = 'notion.py'
AUTHOR = 'yagisann'
URL = 'https://github.com/yagisann/notion.py'
DOWNLOAD_URL = URL
VERSION = '0.1.0'
PYTHON_REQUIRES = '>=3.10'
PACKAGES = [
    'notion',
    'notion.models',
    'notion.builders'
]

def requirements(fname="./requirements.txt"):
    with open(fname, "r") as f:
        r = f.read().splitlines()
    return r

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    maintainer=AUTHOR,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    install_requires=requirements()
)