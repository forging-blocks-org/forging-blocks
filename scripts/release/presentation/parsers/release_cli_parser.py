from argparse import ArgumentParser, Namespace
from typing import Sequence

from scripts.release.domain.value_objects.release_level import ReleaseLevelEnum


class ReleaseCliParser:
    def __init__(self) -> None:
        self._argument_parser = self._create_argument_parser()

    def parse(self, argv: Sequence[str] | None = None) -> Namespace:
        return self._argument_parser.parse_args(argv)

    def _create_argument_parser(self) -> ArgumentParser:
        parser = ArgumentParser(
            prog="release",
            description="Release automation CLI (presentation layer).",
        )

        parser.add_argument(
            "level",
            choices=[level.value for level in ReleaseLevelEnum],
            nargs="?",
            default="patch",
            type=str,
            help="Release level: major, minor, or patch.",
        )

        parser.add_argument(
            "--execute",
            action="store_true",
            default=False,
            help="Execute the release with side effects (default is a simulation).",
        )

        return parser
