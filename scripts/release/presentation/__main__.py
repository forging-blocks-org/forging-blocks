import asyncio
from typing import Sequence

from scripts.release.presentation.container import Container
from scripts.release.presentation.parsers.release_cli_parser import ReleaseCliParser
from scripts.release.presentation.presenters.release_cli_presenter import ReleaseCliPresenter


async def main(argv: Sequence[str] | None = None) -> None:
    container = Container()
    await container.initialize()

    parser = ReleaseCliParser()
    presenter = ReleaseCliPresenter(parser, container)
    await presenter.present(argv)


if __name__ == "__main__":
    asyncio.run(main())
