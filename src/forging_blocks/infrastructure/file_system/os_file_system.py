"""Operating-system file system implementation of the FileSystemPort port.

Uses Python 3.14+ ``asyncio.to_thread()`` to wrap blocking ``pathlib``
and ``os`` calls, avoiding external dependencies like ``aiofiles``.
"""

import asyncio
from pathlib import Path

from forging_blocks.application.ports.outbound.file_system import FileSystemPort


class OSFileSystem(FileSystemPort):
    """File system implementation backed by ``pathlib`` + ``asyncio.to_thread``."""

    async def read(self, path: Path | str) -> bytes:
        """Read file contents as bytes."""
        target = Path(path)
        return await asyncio.to_thread(target.read_bytes)

    async def write(self, path: Path | str, data: bytes) -> None:
        """Write bytes to a file, creating parent directories."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(target.write_bytes, data)

    async def delete(self, path: Path | str) -> None:
        """Delete a file."""
        target = Path(path)
        await asyncio.to_thread(target.unlink)

    async def exists(self, path: Path | str) -> bool:
        """Check if a path exists."""
        target = Path(path)
        return await asyncio.to_thread(target.exists)

    async def list_dir(self, path: Path | str) -> list[Path]:
        """List directory contents."""
        target = Path(path)
        return await asyncio.to_thread(lambda: list(target.iterdir()))
