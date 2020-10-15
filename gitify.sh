#!/bin/bash

git init
find * -size +4M -type f -print >> .gitignore
git add -A
git commit -m "first commit"
git branch -M main
git remote add origin https://raychorn:872f476942dd6ce3821b882b7ddfb1095561d745@github.com/raychorn/svn_python-django-projects.git
git push -u origin main
