#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

log "Building package"
rm -rf dist
poetry build

log "Installing Twine"
python -m pip install --quiet twine

shopt -s nullglob
wheel_files=(dist/*.whl)
sdist_files=(dist/*.tar.gz)
[[ "${#wheel_files[@]}" -eq 1 ]] || fail "Expected exactly one wheel artifact"
[[ "${#sdist_files[@]}" -eq 1 ]] || fail "Expected exactly one source artifact"

log "Validating artifact metadata"
twine check "${wheel_files[0]}" "${sdist_files[0]}"

validation_dir="$(mktemp -d)"
trap 'rm -rf "$validation_dir"' EXIT

validate_installed_artifact() {
  local artifact="$1"
  local target_dir="$2"
  python -m pip install --quiet --no-deps --target "$target_dir" "$artifact"
  EXPECTED_VERSION="$(poetry version -s)" PYTHONPATH="$target_dir" python - <<'PY'
import importlib
import os
from importlib.metadata import Distribution, distribution
from types import ModuleType
from typing import cast
expected_version: str = os.environ["EXPECTED_VERSION"]
package: Distribution = distribution("forging-blocks")
if package.version != expected_version:
    raise SystemExit(f"Artifact version mismatch: {package.version} != {expected_version}")
if package.metadata["Requires-Python"] != ">=3.14":
    raise SystemExit("Artifact Requires-Python metadata is incorrect")
if package.requires:
    raise SystemExit(f"Unexpected runtime dependencies: {package.requires}")
if list(package.entry_points):
    raise SystemExit("Unexpected console entry points found")

package_module: ModuleType = importlib.import_module("forging_blocks")
if package_module.__version__ != expected_version:
    raise SystemExit("Package __version__ does not match artifact metadata")

facade_names: tuple[str, ...] = (
    "forging_blocks",
    "forging_blocks.foundation",
    "forging_blocks.domain",
    "forging_blocks.application",
    "forging_blocks.application.ports",
    "forging_blocks.infrastructure",
    "forging_blocks.presentation",
)
for facade_name in facade_names:
    facade: ModuleType = importlib.import_module(facade_name)
    export_names: tuple[str, ...] = cast(
        tuple[str, ...],
        getattr(facade, "__all__", ()),
    )
    for symbol_name in export_names:
        getattr(facade, symbol_name)
PY
}

log "Installing and checking wheel outside source checkout"
validate_installed_artifact "${wheel_files[0]}" "$validation_dir/wheel"

log "Installing and checking source archive outside source checkout"
validate_installed_artifact "${sdist_files[0]}" "$validation_dir/sdist"

log "Artifacts validated successfully"
