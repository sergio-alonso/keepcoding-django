#!/bin/bash
set -euo pipefail

curl -L https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz | sudo tar zxv -C /usr/local/bin

exit 0
