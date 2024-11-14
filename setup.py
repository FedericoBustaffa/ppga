from setuptools import find_packages, setup

setup(
    name="ppga",
    version="0.0.3",
    package_dir={"": "ppga"},
    packages=find_packages(where="ppga"),
    url="https://github.com/FedericoBustaffa/ppga",
    author="FedericoBustaffa",
    install_requires=["psutil", "colorama", "psutil"],
)
