"""
Install sciparse tools.
"""

# Imports
from setuptools import setup, find_packages

# 
if __name__ == '__main__':

    # Install
    setup(
        name='sciparse',
        version='0.1',
        packages=find_packages(),
        package_data={
            '' : [
                'tests/fixtures/citparse/*.json',
                'tests/fixtures/refparse/*.json',
            ]
        },
        include_package_data=True,
    )

