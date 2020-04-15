#!/bin/bash

# bumps version and commits add a tag

set -ex

previous_version=$(semversioner current-version)
semversioner release
new_version=$(semversioner current-version)

echo "Generating CHANGELOG.md file..."
semversioner changelog > CHANGELOG.md

# Use new version in the pipe.yml metadata file
echo "Replace version '$previous_version' to '$new_version' in setup.py ..."
sed -i 's/version="'${previous_version}'"/version="'${new_version}'"/g' setup.py

# Tag and push
tag="v$(semversioner current-version)"

git tag -a -m "Tagging for release ${tag}" "${tag}"
git add --all
git commit -m "bump version and tag ${tag}"
git push
git push origin ${tag}
	
