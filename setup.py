from setuptools import find_packages, setup

setup(
    name="dagster_mflix",
    packages=find_packages(exclude=["dagster_mflix_tests"]),
    install_requires=[
        "dagster>=1.10.0",
        "dagster-cloud>=1.10.0",
        "dagster-snowflake>=0.26.0",
        "pymongo>=4.3.3",
        "dlt[snowflake]>=0.3.5",
        "scikit-learn==1.5.0",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)