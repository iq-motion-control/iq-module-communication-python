#!/bin/bash

git submodule update --init # required to initialize submodules in Bitbucket Pipeline
python setup.py sdist  
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz

twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD  dist/*