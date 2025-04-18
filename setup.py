from setuptools import find_packages, setup

setup(
    name="ppga",
    version="0.0.3",
    packages=find_packages(),
    url="https://github.com/FedericoBustaffa/ppga",
    author="FedericoBustaffa",
    requires=["setuptool", "wheel"],
    install_requires=["psutil", "colorama", "numpy", "tqdm"],
)
