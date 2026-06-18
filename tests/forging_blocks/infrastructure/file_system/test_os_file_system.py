"""
Tests for the OSFileSystem implementation.
"""

from pathlib import Path

import pytest

from forging_blocks.application.ports.outbound.file_system import FileSystem
from forging_blocks.infrastructure.file_system.os_file_system import OSFileSystem


class TestFileSystemPort:
    """Tests for the FileSystem protocol."""

    def test_filesystem_is_protocol(self):
        """Test that FileSystem is a protocol."""
        assert hasattr(FileSystem, "__protocol_attrs__")

    def test_filesystem_methods(self):
        """Test that FileSystem has required methods."""
        assert "read" in FileSystem.__protocol_attrs__
        assert "write" in FileSystem.__protocol_attrs__
        assert "delete" in FileSystem.__protocol_attrs__
        assert "exists" in FileSystem.__protocol_attrs__
        assert "list_dir" in FileSystem.__protocol_attrs__


class TestOSFileSystem:
    """Tests for the OSFileSystem implementation."""

    @pytest.fixture
    def fs(self):
        """Create an OSFileSystem instance."""
        return OSFileSystem()

    @pytest.mark.asyncio
    async def test_write_and_read(self, fs, tmp_path: Path):
        """Test writing and reading a file."""
        file_path = tmp_path / "test.txt"
        data = b"Hello, World!"

        await fs.write(file_path, data)
        result = await fs.read(file_path)

        assert result == data

    @pytest.mark.asyncio
    async def test_write_creates_parent_dirs(self, fs, tmp_path: Path):
        """Test that write creates parent directories."""
        file_path = tmp_path / "a" / "b" / "c" / "file.txt"
        data = b"nested"

        await fs.write(file_path, data)

        assert await fs.exists(file_path)
        result = await fs.read(file_path)
        assert result == data

    @pytest.mark.asyncio
    async def test_delete(self, fs, tmp_path: Path):
        """Test deleting a file."""
        file_path = tmp_path / "delete_me.txt"
        await fs.write(file_path, b"to delete")

        assert await fs.exists(file_path)

        await fs.delete(file_path)

        assert not await fs.exists(file_path)

    @pytest.mark.asyncio
    async def test_delete_nonexistent_raises(self, fs, tmp_path: Path):
        """Test deleting a non-existent file raises FileNotFoundError."""
        file_path = tmp_path / "ghost.txt"

        with pytest.raises(FileNotFoundError):
            await fs.delete(file_path)

    @pytest.mark.asyncio
    async def test_exists(self, fs, tmp_path: Path):
        """Test checking if a path exists."""
        file_path = tmp_path / "exists.txt"

        assert not await fs.exists(file_path)

        await fs.write(file_path, b"data")

        assert await fs.exists(file_path)

    @pytest.mark.asyncio
    async def test_exists_directory(self, fs, tmp_path: Path):
        """Test checking if a directory exists."""
        assert await fs.exists(tmp_path)

    @pytest.mark.asyncio
    async def test_list_dir(self, fs, tmp_path: Path):
        """Test listing directory contents."""
        (tmp_path / "file1.txt").write_text("1")
        (tmp_path / "file2.txt").write_text("2")
        (tmp_path / "subdir").mkdir()

        entries = await fs.list_dir(tmp_path)

        assert len(entries) == 3
        names = {e.name for e in entries}
        assert names == {"file1.txt", "file2.txt", "subdir"}

    @pytest.mark.asyncio
    async def test_list_dir_nonexistent_raises(self, fs, tmp_path: Path):
        """Test listing a non-existent directory raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            await fs.list_dir(tmp_path / "nonexistent")

    async def test_list_dir_file_raises(self, fs, tmp_path: Path):
        """Test listing a file raises NotADirectoryError."""
        file_path = tmp_path / "file.txt"
        await fs.write(file_path, b"data")

        with pytest.raises(NotADirectoryError):
            await fs.list_dir(file_path)

    @pytest.mark.asyncio
    async def test_read_nonexistent_raises(self, fs, tmp_path: Path):
        """Test reading a non-existent file raises FileNotFoundError."""
        file_path = tmp_path / "ghost.txt"

        with pytest.raises(FileNotFoundError):
            await fs.read(file_path)
