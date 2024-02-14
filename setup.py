import os

from setuptools import setup

import server

with open(os.path.abspath("./README.md", "r")) as file:
    readme = file.read()


setup(
    name="PyCordHTTPServer",
    version=server.__version__,
    description="Fuck you Biatch",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/AusiPlayz",
    author=server.__author__,
    license=server.__license__,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=["server"],
    include_package_data=True,
    #install_requires=["aiohttp", "py-cord"]
)
