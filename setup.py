#!/usr/bin/env python
import pathlib
from platform import python_version
from setuptools import setup, find_packages
import sys
import distutils.cmd
import distutils.log
import subprocess
import typing

project_name = "evalsys"


def find_all_source_files():
    base_files = ["src", "tests"]
    for file in base_files:
        if file.endswith(".py"):
            yield file
        for path in pathlib.Path(file).rglob("*.py"):
            yield str(path)


def generate_simple_command(
    bin: str,
    desc: str,
    args: typing.Iterable[str] | None = None,
):
    class SimpleCommand(distutils.cmd.Command):
        description = desc
        user_options: list[str] = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            command = [bin]

            if args:
                command += list(args)
            self.announce(
                f"Running command: {' '.join(command)}", level=distutils.log.INFO
            )
            subprocess.check_call(command)

    return SimpleCommand


MypyCommand = generate_simple_command(
    "mypy", "run mypy on Python source files", find_all_source_files()
)

BlackCommand = generate_simple_command(
    "black", "run black on Python source files", find_all_source_files()
)

TestCommand = generate_simple_command(
    "pytest",
    "run pytest",
    [f"--cov={project_name}", str(pathlib.Path("tests").resolve())],
)

with open(".python-version", "r") as f:
    prj_pyver_str = f.read().strip()
    prj_pyver_tuple = tuple([int(x) for x in prj_pyver_str.split(".")])
    bin_pyver_tuple = tuple([int(x) for x in python_version().split(".")])
    if bin_pyver_tuple < prj_pyver_tuple:
        sys.exit(f"Sorry, Python < {prj_pyver_str} is not supported")


with open("requirements.txt", "r") as f:
    required_packages = f.read().strip().split()

setup_info = dict(
    name=project_name,
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
    cmdclass={
        "mypy": MypyCommand,
        "black": BlackCommand,
        "test": TestCommand,
    },
)
setup(**setup_info)
