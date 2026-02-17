from setuptools import setup, find_packages

setup(
    name="AURELION Memory-Liteemory-lite",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "networkx>=3.0",
        "pyyaml>=6.0",
        "rich>=13.0",
        "click>=8.0",
    ],
    author="Chase (chase-key)",
    description="A 5-floor library-based knowledge management system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chase-key/AURELION Memory-Liteemory-lite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
