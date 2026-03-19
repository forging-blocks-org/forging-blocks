"""ForgingBlocks package initialization."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("forging-blocks")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
