import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="request-metrics-andresmweber",
    version="0.0.1",
    author="Andres Weber",
    author_email="andresmweber@gmail.com",
    description="A small library for reporting metrics on requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andresmweber/request-metrics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "click==6.7",
        "aiohttp==3.6.2",
        "requests==2.23.0"
    ],
    python_requires='>=3.6',
)
