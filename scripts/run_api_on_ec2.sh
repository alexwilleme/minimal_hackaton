#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

cd ..
export PYTHONPATH=$(pwd)

poetry run python main.py
