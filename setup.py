import setuptools
import os
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

file_path = os.path.join(Path('.'),"requirements.txt")
import pkg_resources
with open(file_path) as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setuptools.setup(
    name="metrics_for_trading",
    version="1.0.1",
    author="InsonusK",
    author_email="insonus.k@gmail.com",
    description="Framework with metrics for trading robots",
    long_description=long_description,
    url="https://github.com/NNTrade/metrics",
    packages=setuptools.find_packages(where="./src"),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)