#!/bin/bash


python setup.py sdist  
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz

twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD  dist/*