#!/bin/bash

# add a tag

set -ex

# Tag and push
tag="v$(semversioner current-version)"

git tag -a -m "Tagging for release ${tag}" "${tag}"
git add --all
git commit -m "bump version and tag ${tag}"
git push
git push origin ${tag}
	
