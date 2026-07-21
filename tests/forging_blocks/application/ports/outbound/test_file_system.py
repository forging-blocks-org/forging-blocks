"""Tests for the FileSystemPort outbound port.

These verify the FileSystemPort protocol contract — not implementation-specific behavior.
"""

import inspect

import pytest

from forging_blocks.application.ports.outbound.file_system_port import FileSystemPort


@pytest.mark.unit
class TestFileSystemPort:
    """Contract tests for the FileSystemPort protocol."""

    def test_filesystem_is_abc(self) -> None:
        """FileSystemPort should be an ABC."""
        from abc import ABC as _ABC

        assert issubclass(FileSystemPort, _ABC)

    def test_filesystem_has_required_methods(self) -> None:
        """FileSystemPort should define read, write, delete, exists, list_dir."""
        assert hasattr(FileSystemPort, "read")
        assert hasattr(FileSystemPort, "write")
        assert hasattr(FileSystemPort, "delete")
        assert hasattr(FileSystemPort, "exists")
        assert hasattr(FileSystemPort, "list_dir")

    def test_filesystem_methods_are_async(self) -> None:
        """All FileSystemPort methods should be async (coroutine functions)."""
        assert inspect.iscoroutinefunction(FileSystemPort.read)
        assert inspect.iscoroutinefunction(FileSystemPort.write)
        assert inspect.iscoroutinefunction(FileSystemPort.delete)
        assert inspect.iscoroutinefunction(FileSystemPort.exists)
        assert inspect.iscoroutinefunction(FileSystemPort.list_dir)

    def test_filesystem_read_signature(self) -> None:
        """read should accept path and return bytes."""
        sig = inspect.signature(FileSystemPort.read)
        params = list(sig.parameters.keys())
        assert "path" in params
        assert sig.return_annotation is bytes

    def test_filesystem_exists_signature(self) -> None:
        """exists should accept Path | str and return bool."""
        sig = inspect.signature(FileSystemPort.exists)
        params = list(sig.parameters.keys())
        assert "path" in params
        assert sig.return_annotation is bool
