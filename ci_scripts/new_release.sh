#!/bin/bash

echo "What type of release (patch, minor, major):"
read RELEASE_TYPE

if [ $RELEASE_TYPE == "patch" ]; then
  echo "You chose: $RELEASE_TYPE"

elif [ $RELEASE_TYPE == "minor" ]; then 
  echo "You chose: $RELEASE_TYPE"

elif [ $RELEASE_TYPE == "major" ]; then 
  echo $RELEASE_TYPE

else
  echo "$RELEASE_TYPE is not a correct type"
  exit
fi


echo "What is the release message:"
read RELEASE_MSG

echo "Creating Release"

RELEASE_BRANCH=release/new_release
git checkout -b ${RELEASE_BRANCH}

semversioner add-change --type $RELEASE_TYPE --description "$RELEASE_MSG" ||
{ echo 'Semversioner Failed' ; 
  git checkout master
  git branch -D release/new_release
  exit 1; }

git add --all
git commit -m "$RELEASE_MSG"
git push --set-upstream origin ${RELEASE_BRANCH}

git checkout master
git branch -D release/new_release