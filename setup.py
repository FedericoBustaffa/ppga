from setuptools import find_packages, setup

setup(
    name="ppga",
    version="0.0.3",
    packages=find_packages(),
    url="https://github.com/FedericoBustaffa/ppga",
    author="FedericoBustaffa",
    install_requires=["setuptools", "wheel", "psutil", "colorama", "numpy", "tqdm"],
)
