"""
Tests for the OSFileSystem implementation.
"""

from pathlib import Path

import pytest

from forging_blocks.application.ports.outbound.file_system_port import FileSystemPort
from forging_blocks.infrastructure.file_system.os_file_system import OSFileSystem


class TestFileSystemPort:
    """Tests for the FileSystemPort protocol."""

    def test_filesystem_is_abc(self) -> None:
        """Test that FileSystemPort is an ABC."""
        from abc import ABC as _ABC

        assert issubclass(FileSystemPort, _ABC)

    def test_filesystem_methods(self) -> None:
        """Test that FileSystemPort has required methods."""
        assert hasattr(FileSystemPort, "read")
        assert hasattr(FileSystemPort, "write")
        assert hasattr(FileSystemPort, "delete")
        assert hasattr(FileSystemPort, "exists")
        assert hasattr(FileSystemPort, "list_dir")


class TestOSFileSystem:
    """Tests for the OSFileSystem implementation."""

    @pytest.fixture
    def fs(self) -> OSFileSystem:
        """Create an OSFileSystem instance."""
        return OSFileSystem()

    async def test_write_and_read(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test writing and reading a file."""
        file_path = tmp_path / "test.txt"
        data = b"Hello, World!"

        await fs.write(file_path, data)
        result: bytes = await fs.read(file_path)

        assert result == data

    async def test_write_creates_parent_dirs(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test that write creates parent directories."""
        file_path = tmp_path / "a" / "b" / "c" / "file.txt"
        data = b"nested"

        await fs.write(file_path, data)

        assert await fs.exists(file_path)
        result: bytes = await fs.read(file_path)
        assert result == data

    async def test_delete(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test deleting a file."""
        file_path = tmp_path / "delete_me.txt"
        await fs.write(file_path, b"to delete")

        assert await fs.exists(file_path)

        await fs.delete(file_path)

        assert not await fs.exists(file_path)

    async def test_delete_nonexistent_raises(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test deleting a non-existent file raises FileNotFoundError."""
        file_path = tmp_path / "ghost.txt"

        with pytest.raises(FileNotFoundError):
            await fs.delete(file_path)

    async def test_exists(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test checking if a path exists."""
        file_path = tmp_path / "exists.txt"

        assert not await fs.exists(file_path)

        await fs.write(file_path, b"data")

        assert await fs.exists(file_path)

    async def test_exists_directory(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test checking if a directory exists."""
        assert await fs.exists(tmp_path)

    async def test_list_dir(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test listing directory contents."""
        (tmp_path / "file1.txt").write_text("1")
        (tmp_path / "file2.txt").write_text("2")
        (tmp_path / "subdir").mkdir()

        entries: list[Path] = await fs.list_dir(tmp_path)

        assert len(entries) == 3
        names: set[str] = {e.name for e in entries}
        assert names == {"file1.txt", "file2.txt", "subdir"}

    async def test_list_dir_nonexistent_raises(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test listing a non-existent directory raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            await fs.list_dir(tmp_path / "nonexistent")

    async def test_list_dir_file_raises(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test listing a file raises NotADirectoryError."""
        file_path = tmp_path / "file.txt"
        await fs.write(file_path, b"data")

        with pytest.raises(NotADirectoryError):
            await fs.list_dir(file_path)

    async def test_read_nonexistent_raises(self, fs: OSFileSystem, tmp_path: Path) -> None:
        """Test reading a non-existent file raises FileNotFoundError."""
        file_path = tmp_path / "ghost.txt"

        with pytest.raises(FileNotFoundError):
            await fs.read(file_path)
