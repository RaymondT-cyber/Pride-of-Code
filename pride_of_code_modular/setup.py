"""
Setup Script - Packaging for Code of Pride.

This module creates distributable packages for the game.
"""

from setuptools import setup, find_packages
import os

# Read the README file for the long description
def read_readme():
    """Read the README file."""
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Get the list of package data files
def get_package_data():
    """Get package data files."""
    package_data = []
    
    # Add assets
    for root, dirs, files in os.walk("assets"):
        for file in files:
            package_data.append(os.path.join(root, file))
            
    # Add docs
    for root, dirs, files in os.walk("docs"):
        for file in files:
            package_data.append(os.path.join(root, file))
            
    return package_data

setup(
    name="code-of-pride",
    version="1.0.0",
    author="Code of Pride Development Team",
    author_email="support@codeofpride.com",
    description="An educational game that teaches Python programming through marching band simulations",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code-of-pride",
    packages=find_packages(),
    package_data={
        '': get_package_data()
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "code-of-pride=core.main:main",
        ],
    },
    keywords="education, programming, python, game, marching band",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/code-of-pride/issues",
        "Documentation": "https://github.com/yourusername/code-of-pride/blob/main/docs/user_guide.md",
        "Source": "https://github.com/yourusername/code-of-pride",
    },
)