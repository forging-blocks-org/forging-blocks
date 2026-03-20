#!/usr/bin/env python3

"""
Validates that every env var expected by a pipeline script
is injected by the workflow step that calls it.

Usage:
    python scripts/pipeline/validate_env_contracts.py

Exit codes:
    0 — all contracts satisfied
    1 — one or more violations found
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

import yaml

# ---------------------------------------------------------------------------
# Domain
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EnvVar:
    name: str


@dataclass(frozen=True)
class ScriptContract:
    script_path: Path
    required_vars: frozenset[EnvVar]


@dataclass(frozen=True)
class WorkflowInjection:
    workflow_path: Path
    job: str
    step: str
    script_path: str
    injected_vars: frozenset[EnvVar]


@dataclass
class Violation:
    workflow_path: Path
    job: str
    step: str
    script_path: str
    missing_vars: frozenset[EnvVar]


@dataclass
class ValidationResult:
    violations: list[Violation] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.violations) == 0


# ---------------------------------------------------------------------------
# Shell contract extractor
# ---------------------------------------------------------------------------

# Matches: [[ -z "$VAR" ]] && fail  /  [ -z "$VAR" ] && fail
_GUARD_PATTERN = re.compile(r'\[\[?\s*-z\s+"?\$\{?([A-Z_][A-Z0-9_]*)\}?"?\s*\]\]?\s*&&\s*fail')

# Matches: ALIAS="${SOURCE_VAR:-}"  — resolves alias back to the injected var name
_ASSIGN_PATTERN = re.compile(
    r'^([A-Z_][A-Z0-9_]*)="\$\{([A-Z_][A-Z0-9_]*):-\}"',
    re.MULTILINE,
)

# Well-known GitHub-provided vars that are never injected by the caller
_GITHUB_BUILTIN: frozenset[str] = frozenset(
    {
        "GITHUB_ENV",
        "GITHUB_OUTPUT",
        "GITHUB_RUN_NUMBER",
        "GITHUB_TOKEN",
        "GITHUB_REF",
        "GITHUB_SHA",
        "GITHUB_WORKSPACE",
        "GITHUB_ACTOR",
        "GITHUB_REPOSITORY",
        "HOME",
        "PATH",
        "ACT",
    }
)


def extract_script_contract(script_path: Path) -> ScriptContract:
    source = script_path.read_text()

    # Build alias map: local_name -> original env var name
    # e.g. BASE_VERSION="${VERSION:-}" -> BASE_VERSION: VERSION
    alias_map: dict[str, str] = {m.group(1): m.group(2) for m in _ASSIGN_PATTERN.finditer(source)}

    required: set[EnvVar] = set()
    for match in _GUARD_PATTERN.finditer(source):
        raw = match.group(1)
        resolved = alias_map.get(raw, raw)
        if resolved not in _GITHUB_BUILTIN:
            required.add(EnvVar(resolved))

    return ScriptContract(script_path=script_path, required_vars=frozenset(required))


# ---------------------------------------------------------------------------
# Workflow injection extractor
# ---------------------------------------------------------------------------

_SCRIPT_CALL_PATTERN = re.compile(
    r"(?:bash\s+|sh\s+|chmod\s+\+x\s+\.\/|\.\/)(scripts/pipeline/[\w./\-]+\.sh)"
)


def _collect_env_block(env_block: dict | None) -> frozenset[EnvVar]:
    if not env_block:
        return frozenset()
    return frozenset(
        EnvVar(str(key))
        for key, value in env_block.items()
        if (str(value).strip() if value is not None else False)
    )


def _find_script_refs(run_block: str) -> Iterator[str]:
    seen: set[str] = set()
    for match in _SCRIPT_CALL_PATTERN.finditer(run_block):
        ref = match.group(1)
        if ref not in seen:
            seen.add(ref)
            yield ref


def extract_workflow_injections(workflow_path: Path) -> list[WorkflowInjection]:
    doc = yaml.safe_load(workflow_path.read_text())
    injections: list[WorkflowInjection] = []

    jobs = doc.get("jobs", {}) or {}
    for job_name, job in jobs.items():
        job_env = _collect_env_block(job.get("env"))
        for step in job.get("steps") or []:
            run_block = step.get("run", "")
            if not run_block:
                continue
            step_env = _collect_env_block(step.get("env"))
            combined_env = job_env | step_env

            for script_ref in _find_script_refs(run_block):
                injections.append(
                    WorkflowInjection(
                        workflow_path=workflow_path,
                        job=job_name,
                        step=step.get("name", "<unnamed>"),
                        script_path=script_ref,
                        injected_vars=combined_env,
                    )
                )

    return injections


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


class EnvContractValidator:
    def __init__(self, scripts_dir: Path, workflows_dir: Path) -> None:
        self._scripts_dir = scripts_dir
        self._workflows_dir = workflows_dir

    def validate(self) -> ValidationResult:
        contracts = self._load_contracts()
        result = ValidationResult()

        for injection in self._load_injections():
            contract = contracts.get(injection.script_path)
            if contract is None:
                continue
            missing = contract.required_vars - injection.injected_vars
            if missing:
                result.violations.append(
                    Violation(
                        workflow_path=injection.workflow_path,
                        job=injection.job,
                        step=injection.step,
                        script_path=injection.script_path,
                        missing_vars=frozenset(missing),
                    )
                )

        return result

    def _load_contracts(self) -> dict[str, ScriptContract]:
        return {
            f"scripts/pipeline/{script.name}": extract_script_contract(script)
            for script in self._scripts_dir.glob("*.sh")
        }

    def _load_injections(self) -> list[WorkflowInjection]:
        return [
            injection
            for workflow in self._workflows_dir.glob("*.yml")
            for injection in extract_workflow_injections(workflow)
        ]


# ---------------------------------------------------------------------------
# Reporter
# ---------------------------------------------------------------------------

_RED = "\033[1;31m"
_GREEN = "\033[1;32m"
_RESET = "\033[0m"


def report(result: ValidationResult) -> None:
    if result.ok:
        print(f"{_GREEN}[OK]{_RESET} All env contracts satisfied")
        return

    print(f"{_RED}[FAIL]{_RESET} Env contract violations found:\n")
    for v in result.violations:
        missing = ", ".join(sorted(var.name for var in v.missing_vars))
        print(f"  {_RED}x{_RESET} {v.workflow_path.name}")
        print(f"    job:  {v.job}")
        print(f'    step: "{v.step}"')
        print(f"    calls: {v.script_path}")
        print(f"    missing vars: {_RED}{missing}{_RESET}")
        print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent.parent
    scripts_dir = repo_root / "scripts" / "pipeline"
    workflows_dir = repo_root / ".github" / "workflows"

    for path, label in ((scripts_dir, "scripts dir"), (workflows_dir, "workflows dir")):
        if not path.exists():
            print(f"{_RED}[ERROR]{_RESET} {label} not found: {path}", file=sys.stderr)
            return 1

    validator = EnvContractValidator(scripts_dir=scripts_dir, workflows_dir=workflows_dir)
    result = validator.validate()
    report(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
