from setuptools import setup, find_packages

setup(
    name="no-weekend-merge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyGithub==1.55",
        "pytz==2021.3",
    ],
    entry_points={
        "console_scripts": [
            "no-out-of-hours-merge = no-out-of-hours-merge:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
