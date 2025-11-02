"""Domain ports module.

Contains inbound and outbound port definitions.
"""

from building_blocks.domain.ports.outbound.read_only_repository import (
    AsyncReadOnlyRepository,
    SyncReadOnlyRepository,
)
from building_blocks.domain.ports.outbound.repository import (
    AsyncRepository,
    SyncRepository,
)
from building_blocks.domain.ports.outbound.write_only_repository import (
    AsyncWriteOnlyRepository,
    SyncWriteOnlyRepository,
)

__all__ = [
    "AsyncRepository",
    "SyncRepository",
    "AsyncReadOnlyRepository",
    "SyncReadOnlyRepository",
    "AsyncWriteOnlyRepository",
    "SyncWriteOnlyRepository",
]
