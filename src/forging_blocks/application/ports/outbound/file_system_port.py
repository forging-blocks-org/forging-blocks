"""File system port for abstract file operations.

Defines the ``FileSystemPort`` protocol that application code depends on,
decoupling file I/O from any specific implementation.
"""

from abc import abstractmethod
from pathlib import Path

from forging_blocks.foundation.ports import OutboundPort


class FileSystemPort(
    OutboundPort[Path | str, bytes],
):
    """Structural protocol for file system operations.
    Any object with ``read``, ``write``, ``delete``, ``exists``,
    and ``list_dir`` async methods satisfies this protocol.
    """

    @abstractmethod
    async def read(self, path: Path | str) -> bytes:
        """Read the contents of a file.

        Args:
            path: Path to the file.

        Returns:
            The file contents as bytes.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        ...

    @abstractmethod
    async def write(self, path: Path | str, data: bytes) -> None:
        """Write data to a file, creating parent directories as needed.

        Args:
            path: Path to the file.
            data: The bytes to write.
        """
        ...

    @abstractmethod
    async def delete(self, path: Path | str) -> None:
        """Delete a file.

        Args:
            path: Path to the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        ...

    @abstractmethod
    async def exists(self, path: Path | str) -> bool:
        """Check whether a file or directory exists.

        Args:
            path: Path to check.

        Returns:
            ``True`` if the path exists, ``False`` otherwise.
        """
        ...

    @abstractmethod
    async def list_dir(self, path: Path | str) -> list[Path]:
        """List the contents of a directory.

        Args:
            path: Path to the directory.

        Returns:
            A list of ``Path`` entries in the directory.

        Raises:
            NotADirectoryError: If *path* is not a directory.
        """
        ...
