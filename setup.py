#!/usr/bin/env python
# type: ignore
import distutils.cmd
import distutils.log
import pathlib
import re
import subprocess
import sys
import typing
from platform import python_version

from setuptools import find_packages, setup

project_name = "evalsys"


def find_all_source_files():
    base_files = ["src", "tests"]
    for file in base_files:
        if file.endswith(".py"):
            yield file
        for path in pathlib.Path(file).rglob("*.py"):
            yield str(path)


def generate_command(
    desc: str | None = None,
    args: list[tuple[str, str, str]] | None = None,
    init_args: typing.Callable[[distutils.cmd.Command], None] | None = None,
    fin_args: typing.Callable[[distutils.cmd.Command], None] | None = None,
    run: typing.Callable[[distutils.cmd.Command], None] | None = None,
):
    if args is None:
        args = []

    class Command(distutils.cmd.Command):
        description = desc or ""
        user_options = args

        def initialize_options(self):
            if init_args:
                init_args(self)

        def finalize_options(self):
            if fin_args:
                fin_args(self)

        def run(self):
            if run:
                run(self)

    return Command


def generate_simple_command(
    bin: str,
    desc: str,
    args: typing.Iterable[str] | None = None,
):
    def run(cmd: distutils.cmd.Command):
        command = [bin]

        if args:
            command += list(args)
        subprocess.check_call(command)

    return generate_command(desc=desc, run=run)


MypyCommand = generate_simple_command(
    "mypy", "run mypy on Python source files", find_all_source_files()
)

FormatCommand = generate_simple_command(
    "darker",
    "run formatter on Python source files",
    ["--isort"] + list(find_all_source_files()) + ["setup.py"],
)

TestCommand = generate_simple_command(
    "pytest",
    "run pytest",
    [f"--cov={project_name}", str(pathlib.Path("tests").resolve())],
)


def version_init(cmd):
    cmd.version = None


def version_fin(cmd):
    assert cmd.version is not None
    pattern = re.compile("^v[0-9]+\\.[0-9]+\\.[0-9]+$")
    assert pattern.match(cmd.version)


def version_run(cmd):
    command = [
        "git",
        "tag",
        "-a",
        cmd.version,
        "-m",
        f"Release of version {cmd.version}",
    ]
    subprocess.check_call(command)

    # Write new version from git
    write_version_from_git()


CreateReleaseVersionCommand = generate_command(
    desc="Tag commit with version",
    args=[("version=", "v", 'Tag name containing "v{MAJOR}.{MINOR}.{PATCH}')],
    init_args=version_init,
    fin_args=version_fin,
    run=version_run,
)


def write_version_from_git():
    command = ["git", "describe", "--tags", "--abbrev=0"]

    version = None
    version_file = f"src/{project_name}/version.py"
    try:
        proc = subprocess.run(command, stdout=subprocess.PIPE, check=True)
        out = proc.stdout.decode("utf-8")

        version = "-".join(out.strip().split("-")).split("v")[1]
    except subprocess.CalledProcessError:
        # Try to read old version from file
        try:
            with open(version_file, "r") as f:
                result = re.search(
                    r"^version = \"([^\"]+)\"$", read_version := f.read()
                )
                if result:
                    version = result.group(1)
                else:
                    raise ValueError("version.py is corrupted. Got:", read_version)
        except FileNotFoundError:
            # Set the version to 0.0.0 if the version can not be read
            # from git and can not be read from an old version file.
            #
            # This can happen, for example, when building in a GitHub Action.
            version = "0.0.0"
            print("Warning: Could not determine package version")

    with open(pathlib.Path(version_file), "w") as f:
        f.write(f'version = "{version}"\n')
    return version


# Retrieves version based on git history (last tagged version)
# and writes it to version.py
version = write_version_from_git()

# Check python binary version
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
    version=version,
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
    include_package_data=True,
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
        "console_scripts": ["evalsys=evalsys.cli:run_cli"],
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=required_packages,
    cmdclass={
        "mypy": MypyCommand,
        "format": FormatCommand,
        "test": TestCommand,
        "release": CreateReleaseVersionCommand,
    },
)
setup(**setup_info)
