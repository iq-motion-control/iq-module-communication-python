#!/bin/bash

cd ..

python setup.py sdist  
pip wheel --no-index --wheel-dir dist dist/*.tar.gz

twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD  dist/*