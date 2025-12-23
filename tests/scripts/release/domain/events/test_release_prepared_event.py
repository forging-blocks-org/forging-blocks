from scripts.release.domain.events.release_prepared_event import ReleasePreparedEvent


class TestReleasePreparedEvent:
    def test_release_prepared_event_creation(self):
        event = ReleasePreparedEvent(version="0.4.2", branch="release/v0.4.2")

        value = event.value
        payload = event._payload

        expected_payload = {
            "version": "0.4.2",
            "branch": "release/v0.4.2",
        }
        assert value == expected_payload
        assert payload == expected_payload
