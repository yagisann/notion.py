from setuptools import setup

DESCRIPTION = 'notion.py: An asynchronous api wrapper and data models for Notion API using pydantic.'
NAME = 'notion.py'
AUTHOR = 'yagisann'
URL = 'https://github.com/yagisann/notion.py'
DOWNLOAD_URL = URL
VERSION = '0.2.0dev'
PACKAGES = [
    'notion',
    'notion.notion_client',
]

def requirements(fname="./requirements.txt"):
    with open(fname, "r") as f:
        r = f.read().splitlines()
    return r

def long_description(fname="./readme.md"):
    with open(fname, "r") as f:
        r = f.read()
    return r

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author=AUTHOR,
    maintainer=AUTHOR,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    install_requires=requirements(),
    python_requires='>=3.11, <4',
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ]
)