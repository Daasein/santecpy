from setuptools import setup, find_packages

setup(
    name="santecpy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pyvisa"],
    author="Daasein",
    author_email="xwei2@binghamton.edu",
    description="A Python package for controlling Santec tunable lasers",
    url="https://github.com/Daasein/santecpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
