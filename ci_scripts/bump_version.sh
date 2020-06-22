#!/usr/bin/env bash

# Bump versions using semversioner

set -ex

previous_version=$(semversioner current-version)
semversioner release
new_version=$(semversioner current-version)

echo "Generating CHANGELOG.md file..."
semversioner changelog > CHANGELOG.md

# Use new version in the pipe.yml metadata file
echo "Replace version '$previous_version' to '$new_version' in setup.py ..."
sed -i 's/version="'${previous_version}'"/version="'${new_version}'"/g' setup.py

