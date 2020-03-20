#!/usr/bin/env python3

import os, re, sys
from setuptools import find_packages, setup


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("Readme.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Sky Moore",
    author_email="mskymoore@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3"
    ],
    description="Terminal application to create a plot of coronavirus data for a user selected location.",
    include_package_data=True,
    install_requires=["requests>=2.22.0","matplotlib>=3.2.1","console-menu>=0.6.0"],
    keywords=["covid", "covid-19", "covid19", "corona", "coronavirus",
              "ncov19", "api", "async", "client"
    ],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="coronavirus-plot",
    packages=find_packages(include=["coronavirus-plot"]),
    url="https://github.com/mskymoore/coronavirus-plot",
    version="1.0.14",
    zip_safe=False,
)
