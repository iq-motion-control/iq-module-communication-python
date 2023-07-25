#!/bin/bash

# required to initialize submodules in Bitbucket Pipeline
sed -i 's/url = \.\.\(.*\)/url = git@bitbucket.org:'"$BITBUCKET_WORKSPACE"'\1/g' ./.gitmodules
git submodule update --init --recursive
sed -i 's/url = git@bitbucket.org:'"$BITBUCKET_WORKSPACE"'/url = \.\./g' ./.gitmodules

python setup.py sdist
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz

twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD  dist/*