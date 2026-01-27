import pytest

from scripts.release.domain.messages.open_pull_request_command import (
    OpenPullRequestCommand,
)


@pytest.mark.unit
class TestOpenPullRequestCommand:
    def test_release_prepared_command_creation(self):
        command = OpenPullRequestCommand(
            version="0.4.2", branch="release/v0.4.2", dry_run=False
        )

        value = command.value
        payload = command._payload
        dry_run = command.dry_run

        expected_payload = {
            "version": "0.4.2",
            "branch": "release/v0.4.2",
            "dry_run": False,
        }
        assert value == expected_payload
        assert payload == expected_payload
        assert dry_run is False
