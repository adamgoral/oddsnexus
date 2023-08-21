from setuptools import find_packages, setup

setup(
    name="oddsnexus_etl_dagster",
    packages=find_packages(exclude=["oddsnexus_etl_dagster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "oddsnexus"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
