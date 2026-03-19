#!/bin/bash
set -e

poetry config repositories.testpypi https://test.pypi.org/legacy/

echo "Validating package $PACKAGE_NAME ($IMPORT_NAME) version $VERSION"
