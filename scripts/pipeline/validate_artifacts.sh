#!/bin/bash
set -e

echo "Building package..."
poetry build

echo "Installing Twine..."
pip install --quiet twine

echo "Validating artifacts..."
twine check dist/*
