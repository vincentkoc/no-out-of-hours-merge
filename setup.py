from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="no-out-of-hours-merge",
    version="1.1.0",
    author_email="vincentkoc@ieee.org",
    description="A GitHub action to restrict PR merges outside "
    + "specified hours, days, and holidays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vincentkoc/no-out-of-hours-merge",
    packages=find_packages(where="src"),
    py_modules=["main"],
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "no-out-of-hours-merge = main:main",
            "no-weekend-merge = main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "PyGithub>=2.9.1",
        "python-dateutil>=2.9.0.post0",
        "pytz>=2026.1.post1",
        "holidays>=0.83",
        "regex>=2026.1.15",
    ],
)
