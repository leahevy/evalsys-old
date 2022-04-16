#!/usr/bin/env python
from platform import python_version
from setuptools import setup, find_packages
import sys

with open(".python-version", "r") as f:
    prj_pyver_str = f.read().strip()
    prj_pyver_tuple = tuple([int(x) for x in prj_pyver_str.split(".")])
    bin_pyver_tuple = tuple([int(x) for x in python_version().split(".")])
    if bin_pyver_tuple < prj_pyver_tuple:
        sys.exit(f"Sorry, Python < {prj_pyver_str} is not supported")


with open("requirements.txt", "r") as f:
    required_packages = f.read().strip().split()

setup_info = dict(
    name="evalsys",
    version="0.0.1",
    author="Leah Lackner",
    author_email="leah.lackner+github@gmail.com",
    url="https://github.com/evyli/evalsys",
    project_urls={
        "Documentation": "https://github.com/evyli/evalsys/blob/master/README.md#evalsys",
        "Source": "https://github.com/evyli/evalsys",
        "Tracker": "https://github.com/evyli/evalsys/issues",
    },
    description="Tool to configure Linux based systems including population of dotfiles and package installation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    platforms="Linux, Mac OSX",
    license="GPLv3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10.3",
    ],
    zip_safe=True,
    entry_points={
        "console_scripts": ["evalsys=evalsys.main:run_typer"],
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=required_packages,
)
setup(**setup_info)
