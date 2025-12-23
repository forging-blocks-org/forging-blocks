from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from scripts.release.presentation import cli


@dataclass(frozen=True)
class _PrepareOut:
    version: str
    branch: str
    tag: str


@dataclass(frozen=True)
class _PrOut:
    pr_id: str | None
    url: str | None


class _PrepareUC:
    def __init__(self) -> None:
        self.calls: list[Any] = []

    async def execute(self, request: Any) -> _PrepareOut:
        self.calls.append(request)
        return _PrepareOut(version="1.2.3", branch="release/v1.2.3", tag="v1.2.3")


class _OpenPrUC:
    def __init__(self) -> None:
        self.calls: list[Any] = []

    async def execute(self, request: Any) -> _PrOut:
        self.calls.append(request)
        return _PrOut(pr_id="123", url="https://example/pr/123")


class _Container:
    def __init__(self) -> None:
        self.prepare_uc = _PrepareUC()
        self.pr_uc = _OpenPrUC()

    def prepare_release_use_case(self) -> _PrepareUC:
        return self.prepare_uc

    def open_release_pull_request_use_case(self) -> _OpenPrUC:
        return self.pr_uc


class _DryPrUC:
    async def execute(self, request):
        return _PrOut(pr_id=None, url=None)


class _DryContainer(_Container):
    def open_release_pull_request_use_case(self):
        return _DryPrUC()


class TestCli:
    def test_run_prepare_when_json_then_prints_json_and_exit_0(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setattr(
            "scripts.release.presentation.cli.Container",
            _Container,
        )

        code = cli.run(["prepare", "--level", "patch", "--dry-run", "--json"])

        assert code == 0
        out = capsys.readouterr().out.strip()
        assert '"version": "1.2.3"' in out
        assert '"branch": "release/v1.2.3"' in out
        assert '"tag": "v1.2.3"' in out

    def test_run_open_pr_when_human_then_prints_lines_and_exit_0(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setattr(
            "scripts.release.presentation.cli.Container",
            _Container,
        )

        code = cli.run(
            [
                "open-pr",
                "--base",
                "main",
                "--head",
                "release/v1.2.3",
                "--title",
                "Release v1.2.3",
                "--body",
                "Notes",
            ]
        )

        assert code == 0
        out = capsys.readouterr().out
        assert "pr_id: 123" in out
        assert "url: https://example/pr/123" in out

    def test_run_when_exception_then_exit_1_and_print_stderr(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        class _BadContainer(_Container):
            def prepare_release_use_case(self):
                raise RuntimeError("boom")

        monkeypatch.setattr(
            "scripts.release.presentation.cli.Container",
            _BadContainer,
        )

        code = cli.run(["prepare", "--level", "patch"])

        assert code == 1
        err = capsys.readouterr().err
        assert "boom" in err

    def test_run_open_pr_dry_run_json(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setattr(
            "scripts.release.presentation.cli.Container",
            _DryContainer,
        )

        code = cli.run(
            [
                "open-pr",
                "--base",
                "main",
                "--head",
                "release/v1.2.3",
                "--title",
                "Release",
                "--body",
                "Notes",
                "--dry-run",
                "--json",
            ]
        )

        assert code == 0
        out = capsys.readouterr().out
        assert '"pr_id": null' in out
        assert '"url": null' in out

    def test_run_prepare_human_output(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setattr(
            "scripts.release.presentation.cli.Container",
            _Container,
        )

        code = cli.run(["prepare", "--level", "patch"])

        assert code == 0
        out = capsys.readouterr().out
        assert "version:" in out
        assert "branch:" in out
        assert "tag:" in out

    def test_run_prepare_dry_run_no_output(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        class _DryPrepareUC:
            async def execute(self, request):
                return None

        class _DryPrepareContainer(_Container):
            def prepare_release_use_case(self):
                return _DryPrepareUC()

        monkeypatch.setattr(
            "scripts.release.presentation.cli.Container",
            _DryPrepareContainer,
        )

        code = cli.run(["prepare", "--level", "patch", "--dry-run"])

        assert code == 0
        out = capsys.readouterr().out
        assert out.strip() == ""

    def test_print_output_with_generic_json_payload(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        cli._print_output(payload={"key": "value"}, as_json=True)
        out = capsys.readouterr().out.strip()
        assert out == '{"key": "value"}'

    def test_print_output_with_generic_human_payload(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        cli._print_output(payload="Some string payload", as_json=False)
        out = capsys.readouterr().out.strip()
        assert out == "Some string payload"

    def test_run_when_command_raises_exception(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        class _ErrorContainer(_Container):
            def prepare_release_use_case(self):
                raise ValueError("Deliberate error")

        monkeypatch.setattr(
            "scripts.release.presentation.cli.Container", _ErrorContainer
        )

        code = cli.run(["prepare", "--level", "patch"])
        assert code == 1  # Exit code for failure
        err = capsys.readouterr().err
        assert "Deliberate error" in err

    def test_main_entry_point(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Mock the run function to avoid actual execution
        def mock_run(argv=None):
            assert argv is None  # The entry point should call it with `None`
            return 0

        monkeypatch.setattr("scripts.release.presentation.cli.run", mock_run)

        # Simulate the script being run as __main__
        with pytest.raises(SystemExit) as exc_info:
            cli.main()
        assert exc_info.value.code == 0

    def test_run_with_unknown_command(self, monkeypatch: pytest.MonkeyPatch) -> None:
        with pytest.raises(SystemExit) as exc_info:
            cli.run(["unknown-command"])
        assert exc_info.value.code == 2

    def test_run_unknown_command_then_raise_system_exit(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        class _BadContainer(_Container):
            pass

        monkeypatch.setattr(
            "scripts.release.presentation.cli.Container",
            _BadContainer,
        )

        with pytest.raises(SystemExit) as exc_info:
            cli.run(["unknown-command"])

        assert exc_info.value.code == 2
        err = capsys.readouterr().err
        assert (
            "usage:" in err
        )  # `argparse` includes "usage:" in its error message for invalid commands
        assert "invalid choice" in err or "unknown-command" in err
