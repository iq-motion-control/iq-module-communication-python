#!/bin/bash

# required to initialize submodules in Bitbucket Pipeline
git submodule update --init

python setup.py sdist
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz

twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD  dist/*