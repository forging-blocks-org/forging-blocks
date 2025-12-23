# from __future__ import annotations
#
# import argparse
# import asyncio
# import json
# import sys
# from dataclasses import asdict
# from typing import Sequence
#
# from scripts.release.application.ports.inbound import (
#     CreateReleasePullRequestInput,
#     PrepareReleaseInput,
# )
# from scripts.release.presentation.container import Container
#
#
# def _build_parser() -> argparse.ArgumentParser:
#     parser = argparse.ArgumentParser(
#         prog="release",
#         description="ForgingBlocks release automation CLI (presentation layer).",
#     )
#
#     sub = parser.add_subparsers(dest="command", required=True)
#
#     prepare = sub.add_parser(
#         "prepare",
#         help="Prepare a release (compute version, create/resume branch, tag, commit, push).",
#     )
#     prepare.add_argument(
#         "--level",
#         required=True,
#         choices=["major", "minor", "patch"],
#         help='Release level ("major" | "minor" | "patch").',
#     )
#     prepare.add_argument(
#         "--dry-run",
#         action="store_true",
#         help="If set, performs validation and computation only (no side effects).",
#     )
#     prepare.add_argument(
#         "--json",
#         action="store_true",
#         help="If set, prints machine-readable JSON.",
#     )
#
#     pr = sub.add_parser(
#         "create-pr",
#         help="Create the release pull request (intent to publish).",
#     )
#     pr.add_argument("--base", required=True, help='Base branch (expected "main").')
#     pr.add_argument(
#         "--head", required=True, help='Head branch (expected "release/vX.Y.Z").'
#     )
#     pr.add_argument("--title", required=True, help="Pull request title.")
#     pr.add_argument("--body", required=True, help="Pull request body.")
#     pr.add_argument(
#         "--dry-run",
#         action="store_true",
#         help="If set, validates inputs but does not call the hosting platform.",
#     )
#     pr.add_argument(
#         "--json",
#         action="store_true",
#         help="If set, prints machine-readable JSON.",
#     )
#
#     return parser
#
#
# def _print_output(*, payload: object, as_json: bool) -> None:
#     if as_json:
#         # dataclasses (DTOs) are supported, else fallback to str().
#         if hasattr(payload, "__dataclass_fields__"):
#             print(json.dumps(asdict(payload)))
#         else:
#             print(json.dumps(payload))  # type: ignore[arg-type]
#         return
#
#     # Human-friendly output
#     if hasattr(payload, "__dataclass_fields__"):
#         d = asdict(payload)
#         for k, v in d.items():
#             print(f"{k}: {v}")
#         return
#
#     print(payload)
#
#
# async def _run_prepare(args: argparse.Namespace, container: Container) -> int:
#     use_case = container.prepare_release_use_case()
#     output = await use_case.execute(
#         PrepareReleaseInput(
#             level=args.level,
#             dry_run=bool(args.dry_run),
#         )
#     )
#     _print_output(payload=output, as_json=bool(args.json))
#     return 0
#
#
# async def _run_create_pr(args: argparse.Namespace, container: Container) -> int:
#     use_case = container.create_release_pull_request_use_case()
#     output = await use_case.execute(
#         CreateReleasePullRequestInput(
#             base=args.base,
#             head=args.head,
#             title=args.title,
#             body=args.body,
#             dry_run=bool(args.dry_run),
#         )
#     )
#     _print_output(payload=output, as_json=bool(args.json))
#     return 0
#
#
# def run(argv: Sequence[str] | None = None) -> int:
#     parser = _build_parser()
#     args = parser.parse_args(list(argv) if argv is not None else None)
#
#     container = Container()
#
#     try:
#         if args.command == "prepare":
#             return asyncio.run(_run_prepare(args, container))
#         if args.command == "create-pr":
#             return asyncio.run(_run_create_pr(args, container))
#         raise RuntimeError(f"Unknown command: {args.command}")
#     except (
#         Exception
#     ) as exc:  # presentation boundary: translate to process exit + stderr
#         print(str(exc), file=sys.stderr)
#         return 1
#
#
# def main() -> None:
#     raise SystemExit(run())
#
#
# if __name__ == "__main__":
#     main()
