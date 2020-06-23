#!/bin/bash

# add a tag

set -ex

# Tag and push
tag="v$(semversioner current-version)"

git tag -a -m "Tagging for release ${tag}" "${tag}"
git push origin ${tag}
	
