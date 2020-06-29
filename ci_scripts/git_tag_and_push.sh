#!/bin/bash

# Commit back to the repository
# version number, push the tag back to the remote.

set -ex

# Tag and push
tag="v$(semversioner current-version)"

git add .
git commit -m "Update files for new version '${tag}'"

git tag -a -m "Tagging for release ${tag}" "${tag}"
git push origin ${tag}
	
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch 
git checkout master 
git merge --no-ff -m "Merge ${BITBUCKET_BRANCH} into master" ${BITBUCKET_BRANCH}
git push origin master
