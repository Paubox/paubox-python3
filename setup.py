import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pauboxpython3",
    version="1.0.0",
    author="Paubox",
    author_email="info@paubox.com",
    description="Python SDK for Paubox Email REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Paubox/paubox-python3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "License :: OSI Approved :: Apache Software License"
    ],
)
