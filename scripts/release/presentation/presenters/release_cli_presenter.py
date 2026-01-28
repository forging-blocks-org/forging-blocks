from logging import Logger
from typing import Sequence

from scripts.release.application.ports.inbound.prepare_release_use_case import PrepareReleaseInput
from scripts.release.presentation.container import Container
from scripts.release.presentation.parsers import ReleaseCliParser


class ReleaseCliPresenter:
    def __init__(self, parser: ReleaseCliParser, container: Container) -> None:
        self._parser = parser
        self._container = container
        self._logger = Logger(__name__)

    async def present(self, argv: Sequence[str] | None = None) -> None:
        self._logger.info("Parsing CLI arguments")

        parsed_input = self._parser.parse(argv)

        dry_run = not parsed_input.execute

        self._logger.info(f"Preparing release with level: {parsed_input.level}, dry_run: {dry_run}")

        service_input = PrepareReleaseInput(level=parsed_input.level, dry_run=dry_run)

        self._logger.debug(f"Service input: {service_input}")

        prepare_release_use_case = self._container.get_prepare_release_use_case()

        service_output = await prepare_release_use_case.execute(service_input)

        self._logger.info("Release preparation completed")
        self._logger.debug(f"Service output: {service_output}")

        if dry_run:
            self._logger.info("Dry run mode - no changes were made")
        else:
            self._logger.info("Release executed successfully")
