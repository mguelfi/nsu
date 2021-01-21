import setuptools
from _version import __version__
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nessusScanUpload",
    version=__version__,
    author="Michael Guelfi",
    author_email="michael.guelfi@defence.gov.au",
    description="Posts scans from Nessus Manager to AWS/Azure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mxguelf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        'sample_config': ['nessus2azure.conf.dist'],
    },
)
