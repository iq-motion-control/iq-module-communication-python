#!/bin/bash

# required to initialize submodules in Bitbucket Pipeline
git config --global user.name "Ben Quan"
git config --global user.enmal "ben.quan@vertiq.co"
git submodule update --init

python setup.py sdist
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz

twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD  dist/*