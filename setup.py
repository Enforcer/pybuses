import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybuses",
    version="1.0.0",
    author="Sebastian Buczyński",
    author_email="nnplaya@gmail.com",
    description="Pythonic Command & Event buses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Enforcer/pybuses",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
