#!/usr/bin/env bats

load './helpers.bash'

@test "prepare fails if no release level is provided" {
  run bash scripts/release/prepare.sh

  [ "$status" -ne 0 ]
  [[ "$output" =~ "release level required" ]]
}
