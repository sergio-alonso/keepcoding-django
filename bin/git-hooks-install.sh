#!/bin/sh

# [Flake8 Version Control Hook](http://flake8.pycqa.org/en/latest/user/using-hooks.html)

flake8 --install-hook git

git config --bool flake8.strict true

exit 0
