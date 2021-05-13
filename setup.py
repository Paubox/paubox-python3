import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paubox-python3",
    version="1.0.0",
    author="Paubox",
    author_email="info@paubox.com",
    description="Python3 SDK for Paubox Email REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Paubox/paubox-python3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License"
    ],
)
