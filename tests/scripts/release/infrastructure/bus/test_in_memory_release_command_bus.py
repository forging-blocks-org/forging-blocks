"""Tests for the in-memory release command bus."""

from unittest.mock import AsyncMock

import pytest
from scripts.release.domain.messages.open_pull_request_command import OpenPullRequestCommand
from scripts.release.infrastructure.bus.in_memory_release_command_bus import (
    InMemoryReleaseCommandBus,
)


@pytest.mark.unit
class TestInMemoryReleaseCommandBus:
    """Test the InMemoryReleaseCommandBus."""

    @pytest.fixture
    def command_bus(self):
        """Create a command bus instance."""
        return InMemoryReleaseCommandBus()

    @pytest.fixture
    def mock_handler(self):
        """Create a mock handler."""
        return AsyncMock()

    @pytest.fixture
    def test_command(self):
        """Create a test command."""
        return OpenPullRequestCommand(version="v0.3.11", branch="release/v0.3.11", dry_run=False)

    async def test_dispatch_calls_send(self, command_bus, test_command, mock_handler):
        """Test that dispatch delegates to send method."""
        # Register a handler
        await command_bus.register(OpenPullRequestCommand, mock_handler)

        # Dispatch the command
        await command_bus.dispatch(test_command)

        # Verify handler's handle method was called
        mock_handler.handle.assert_called_once_with(test_command)

    async def test_register_and_send(self, command_bus, test_command, mock_handler):
        """Test registering a handler and sending a command."""
        # Register handler
        await command_bus.register(OpenPullRequestCommand, mock_handler)

        # Send command
        await command_bus.send(test_command)

        # Verify handler's handle method was called
        mock_handler.handle.assert_called_once_with(test_command)
