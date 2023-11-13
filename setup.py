from pathlib import Path

from setuptools import find_packages, setup

from _version import __version__

setup(
    name="randinator",
    version=__version__,
    author="André Graça",
    author_email="",
    description="A tool to create random items",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={"": ["data/*.txt"]},
    platforms="Python",
)
