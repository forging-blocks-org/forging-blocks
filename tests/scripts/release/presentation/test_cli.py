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


class _CreatePrUC:
    def __init__(self) -> None:
        self.calls: list[Any] = []

    async def execute(self, request: Any) -> _PrOut:
        self.calls.append(request)
        return _PrOut(pr_id="123", url="https://example/pr/123")


class _Container:
    def __init__(self) -> None:
        self.prepare_uc = _PrepareUC()
        self.pr_uc = _CreatePrUC()

    def prepare_release_use_case(self) -> _PrepareUC:
        return self.prepare_uc

    def create_release_pull_request_use_case(self) -> _CreatePrUC:
        return self.pr_uc


class _DryPrUC:
    async def execute(self, request):
        return _PrOut(pr_id=None, url=None)


class _DryContainer(_Container):
    def create_release_pull_request_use_case(self):
        return _DryPrUC()


class TestCli:
    def test_run_prepare_when_json_then_prints_json_and_exit_0(
        self, monkeypatch, capsys
    ) -> None:
        monkeypatch.setattr(cli, "Container", _Container)

        code = cli.run(["prepare", "--level", "patch", "--dry-run", "--json"])

        assert code == 0
        out = capsys.readouterr().out.strip()
        assert '"version": "1.2.3"' in out
        assert '"branch": "release/v1.2.3"' in out
        assert '"tag": "v1.2.3"' in out

    def test_run_create_pr_when_human_then_prints_lines_and_exit_0(
        self, monkeypatch, capsys
    ) -> None:
        monkeypatch.setattr(cli, "Container", _Container)

        code = cli.run(
            [
                "create-pr",
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
        self, monkeypatch, capsys
    ) -> None:
        class _BadContainer(_Container):
            def prepare_release_use_case(self):
                raise RuntimeError("boom")

        monkeypatch.setattr(cli, "Container", _BadContainer)

        code = cli.run(["prepare", "--level", "patch"])

        assert code == 1
        err = capsys.readouterr().err
        assert "boom" in err

    def test_run_when_unknown_command_then_exit_2(self) -> None:
        with pytest.raises(SystemExit) as exc:
            cli.run(["unknown-command"])

        assert exc.value.code == 2

    def test_run_create_pr_dry_run_json(self, monkeypatch, capsys) -> None:
        monkeypatch.setattr(cli, "Container", _DryContainer)

        code = cli.run(
            [
                "create-pr",
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

    def test_run_prepare_human_output(self, monkeypatch, capsys) -> None:
        monkeypatch.setattr(cli, "Container", _Container)

        code = cli.run(["prepare", "--level", "patch"])

        assert code == 0
        out = capsys.readouterr().out
        assert "version:" in out
        assert "branch:" in out
        assert "tag:" in out
