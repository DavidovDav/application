#!/bin/bash
git -l
git tag -l | xargs -n 1 git push --delete origin
git tag | xargs git tag -d
git tag -l