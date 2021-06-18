import re

import setuptools
import unittest


def test_suite():
    return unittest.TestLoader().discover("tests", pattern="test_*.py")


with open("readme.md", "r") as fh:
    long_description = fh.read()

_version_regex = (
    r"^__version__ = ('|\")((?:[0-9]+\.)*[0-9]+(?:\.?([a-z]+)(?:\.?[0-9])?)?)\1$"
)

with open("./discord/ext/levelling/__init__.py") as stream:
    match = re.search(_version_regex, stream.read(), re.MULTILINE)

version = match.group(2)

setuptools.setup(
    name="discord.ext.levelling",
    version=version,
    author="Menudocs",
    author_email="contact@menudocs.org",
    description="An easy to use package for levelling features in discord.py.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MenuDocs/discord.ext.levelling",
    packages=setuptools.find_packages(),
    install_requires=["discord.py>=1", "aiosqlite"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.8",
    test_suite="setup.test_suite",
)
