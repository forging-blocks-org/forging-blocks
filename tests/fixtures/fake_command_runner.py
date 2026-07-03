"""Fake CommandRunner implementation for infrastructure tests.

Configurable responses replace real subprocess calls. Tests verify
behaviour through recorded calls and configured outputs, not
through mock interaction assertions.
"""

from scripts.release.infrastructure.commons.process import CommandRunner


class FakeCommandRunner(CommandRunner):
    """State-based CommandRunner fake.

    ``responses`` is an ordered list — each ``run()`` call pops the
    first entry.  Entries may be a ``str`` (success) or an
    ``Exception`` to raise.
    """

    def __init__(self, *configured_outputs: str | Exception) -> None:
        self.configured_outputs: list[str | Exception] = list(configured_outputs)
        self.calls: list[tuple[list[str], bool, bool]] = []

    def run(
        self,
        cmd: list[str],
        *,
        check: bool = True,
        suppress_error_log: bool = False,
    ) -> str:
        self.calls.append((cmd, check, suppress_error_log))

        if not self.configured_outputs:
            return ""

        output = self.configured_outputs.pop(0)
        if isinstance(output, Exception):
            raise output
        return output
