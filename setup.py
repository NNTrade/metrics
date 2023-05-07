import pkg_resources
import setuptools
import os
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

file_path = os.path.join(Path('.'), "requirements.txt")
install_requires = []
with open(file_path) as requirements_txt:
    for requirement in pkg_resources.parse_requirements(requirements_txt):
        install_requires.append(str(requirement))
        
print(install_requires)

lib = "NNTrade.metric"

setuptools.setup(
    name=lib,
    version="4.3.1",
    author="InsonusK",
    author_email="insonus.k@gmail.com",
    description="Framework with metrics for trading robots",
    long_description=long_description,
    url="https://github.com/NNTrade/metrics",
    packages=[f"{lib}.{pkg}" for pkg in setuptools.find_packages(where="src")],
    package_dir={lib: 'src'},
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
