from setuptools import setup, find_packages

setup(
    name="aurelion-memory-lite",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "networkx>=3.0",
        "pyyaml>=6.0",
        "rich>=13.0",
        "click>=8.0",
    ],
    extras_require={
        "mcp": ["mcp>=1.0.0"],
    },
    entry_points={
        "console_scripts": [
            "aurelion-memory-mcp=aurelion_memory_mcp.__main__:main",
        ],
    },
    author="chase-key",
    description="A 5-floor library-based knowledge management system with MCP server support",
    long_description=open("README.md", encoding="utf-8", errors="ignore").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chase-key/aurelion-memory-lite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
