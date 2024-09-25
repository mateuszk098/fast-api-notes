from setuptools import find_packages, setup

setup(
    name="cryptids-app",
    version="1.0.0",
    package_dir={"": "."},
    packages=find_packages(where="."),
)
