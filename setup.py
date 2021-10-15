from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atomd",
    version="0.2.5",
    description="A markdown lexer and parser which gives the programmer atomic control over markdown parsing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stonepresto/atomd",
    author="stonepresto",
    author_email="stonepresto@darkbyte.io",
    license="GPLv3",
    project_urls={
        'Bug Tracker': 'https://github.com/stonepresto/atomd/issues',
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
)
