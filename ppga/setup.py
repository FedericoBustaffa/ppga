from setuptools import find_packages, setup

setup(
    name="ppga",
    version="0.0.3",
    package_dir={"": "."},
    packages=find_packages(where="."),
    url="https://github.com/FedericoBustaffa/ppga",
    author="FedericoBustaffa",
    install_requires=["psutil", "colorama", "psutil"],
)
