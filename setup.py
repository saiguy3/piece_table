try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open("README.rst", "r") as f:
    long_description = f.read()


setup(
    name="piece_table",
    version="0.0.2",
    description="A Python implementation of the piece table data structure",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Sai Atmakuri",
    author_email="saiatmakuri@yahoo.com",
    url="https://github.com/saiguy3/piece_table",
    packages=["piece_table"],
    license="MIT",
    python_requires=">=3",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    keywords=["piecetable", "table"],
)
