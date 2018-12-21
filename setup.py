from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='pydp',
 version='0.0.1',
 author="Digital Proteomics",
 author="info@digitalproteomics.com",
 description="Python scripts at dp",
 long_description=long_description,
 long_description_content_type="text/markdown",
 packages=setuptools.find_packages(),
 classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
     ],
 py_modules=['pydp'])
