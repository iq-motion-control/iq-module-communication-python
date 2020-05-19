#!/bin/bash

# Commit back to the repository
# version number, push the tag back to the remote.

set -ex

# Tag and push
tag="v$(semversioner current-version)"

RELEASE_BRANCH=release/$tag
git checkout -b ${RELEASE_BRANCH} master
# git add ./dist/
# git commit -m "Creating new release '${tag}'"
# git push 
