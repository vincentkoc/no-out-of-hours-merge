from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="no-weekend-merge",
    version="0.1.0",
    author_email="vincentkoc@ieee.org",
    description="A GitHub action to restrict PR merges outside specified hours, days, and holidays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koconder/no-out-of-hours-merge",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "no-out-of-hours-merge = no-out-of-hours-merge:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=[
        "github3.py>=2.0.0",
        "python-dateutil>=2.8.1",
        "pytz>=2021.1",
        "holidays>=0.11.3",
    ],
)
