import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='dcipher',
    version='0.1',
    author="Dery Rahman A",
    author_email="dery.ra@gmail.com",
    description="Cipher for fun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deryrahman/dcipher",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
