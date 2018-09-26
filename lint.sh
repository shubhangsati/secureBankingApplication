#!/bin/bash

echo -ne "Fixing lint errors..."
autopep8 --in-place --recursive --aggressive .
echo -e "...Done\n" 
echo "Checking for unfixed/other errors..."
pycodestyle
echo -e "\nDone"