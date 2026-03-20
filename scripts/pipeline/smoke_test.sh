#!/bin/bash
set -e

echo "Running smoke test..."

sleep 15
TMP_VENV=$(mktemp -d)
python3 -m venv "$TMP_VENV"
source "$TMP_VENV/bin/activate"

pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            "${{ env.PACKAGE_NAME }}==${{ env.PUBLISH_VERSION }}"

python - <<EOF
import ${{ env.IMPORT_NAME }}
from importlib.metadata import version
v = version("${{ env.PACKAGE_NAME }}")
print(f"Detected Version: {v}")
assert v == "${{ env.PUBLISH_VERSION }}"
EOF
