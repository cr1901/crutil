from setuptools import setup, find_packages

setup(
    name="crutil",
    version="0.1.0",
    description="Notebook utility functions.",
    long_description=open("README.md").read(),
    url="https://github.com/cr1901/crutil",
    author="William D. Jones",
    author_email="thor0505@comcast.net",
    # license="0-clause BSD License",
    packages=find_packages(exclude=["tests"]),
    platforms=["Any"],
    # classifiers=[
    #     "Development Status :: 3 - Alpha",
    #     "Environment :: Console",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: BSD License",
    #     "Topic :: System :: Emulators",
    #     "Programming Language :: Python :: 3.5",
    #     "Programming Language :: Python :: 3.6",
    #     "Programming Language :: Python :: 3.7"
    # ],
)
