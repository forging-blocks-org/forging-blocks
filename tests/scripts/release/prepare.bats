#!/usr/bin/env bats
bats_require_minimum_version 1.5.0

load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'

setup() {
  REPO="$(mktemp -d)"
  cd "$REPO"

  git init -q
  git config user.email "test@example.com"
  git config user.name "Test User"

  cat > pyproject.toml <<EOF
[tool.poetry]
name = "test"
version = "0.1.0"
EOF

  git add pyproject.toml
  git commit -qm "init"

  export PATH="$BATS_TEST_DIRNAME/../../../scripts/release:$PATH"
}

teardown() {
  git tag -d v0.1.1 >/dev/null 2>&1 || true
  git checkout main >/dev/null 2>&1 || true
  git branch -D release/v0.1.1 >/dev/null 2>&1 || true
}


@test "prepare.sh can be re-run after branch creation" {
  run bash "$BATS_TEST_DIRNAME/../../../scripts/release/prepare.sh" patch
  assert_success

  # Simulate failure *after* branch creation
  git checkout main -q

  # Re-run should succeed
  run bash "$BATS_TEST_DIRNAME/../../../scripts/release/prepare.sh" patch
  assert_success
}

@test "prepare.sh can be re-run after commit already exists" {
  run bash "$BATS_TEST_DIRNAME/../../../scripts/release/prepare.sh" patch
  assert_success

  # Branch exists, commit exists
  git checkout main -q

  run bash "$BATS_TEST_DIRNAME/../../../scripts/release/prepare.sh" patch
  assert_success
}

@test "prepare.sh fails if tag already exists" {
  git tag "v0.1.1"

  run -1 "$BATS_TEST_DIRNAME/../../../scripts/release/prepare.sh" patch
  assert_output --partial "ERROR: tag already exists"
}
