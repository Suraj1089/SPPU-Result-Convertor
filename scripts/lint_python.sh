#!/bin/bash

# Run pylint
echo "Running pylint..."
# shellcheck disable=SC2035
pylint *

# Run flake8 excluding the venv directory
echo "Running flake8..."
flake8 --exclude=venv
