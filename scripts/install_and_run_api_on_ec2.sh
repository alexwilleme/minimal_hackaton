#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# fixme: this must be done manually as it's loading this script - should be part of the docker image
# aws s3 cp s3://alex-willeme-bucket/backend.zip .
# unzip backend.zip -d backend/
# cd backend/scripts/
# bash install_and_run_api_on_ec2.sh

cd ..

poetry config virtualenvs.in-project true
poetry install

export PYTHONPATH=$(pwd)

poetry run python main.py
