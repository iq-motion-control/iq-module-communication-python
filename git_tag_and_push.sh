#!/bin/bash

# Commit back to the repository
# version number, push the tag back to the remote.

set -ex

# Tag and push
tag="v$(semversioner current-version)"

RELEASE_BRANCH=release/$tag
git checkout -b ${RELEASE_BRANCH}
git add .
git commit -m "Update files for new version '${tag}'"

git tag -a -m "Tagging for release ${tag}" "${tag}"
git push origin ${tag}
	
git checkout ${BITBUCKET_BRANCH}
git merge --no-ff -m "Merge ${RELEASE_BRANCH} into ${BITBUCKET_BRANCH} [skip ci]" ${RELEASE_BRANCH}
git push origin ${BITBUCKET_BRANCH}
