#!/usr/bin/env bats

load './helpers.bash'

@test "dry_run prints next version information" {
  run bash scripts/release/dry_run.sh patch

  [ "$status" -eq 0 ]
  [[ "$output" =~ "DRY RUN" ]]
  [[ "$output" =~ "Next version" ]]
  [[ "$output" =~ "release/v" ]]
}
