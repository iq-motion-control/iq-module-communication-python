#!/usr/bin/env bash

# Bump versions using semversioner

set -ex

previous_version=$(semversioner current-version)

semversioner release

new_version=$(semversioner current-version)

echo "Generating CHANGELOG.md file..."
semversioner changelog > CHANGELOG.md

# Use new version in the README.md examples
echo "Replace version '$previous_version' to '$new_version' in README.md ..."
sed -i "s/$previous_version/$new_version/g" README.md

# Use new version in the pipe.yml metadata file
echo "Replace version '$previous_version' to '$new_version' in pipe.yml ..."
sed -i "s/$previous_version/$new_version/g" setup.py
