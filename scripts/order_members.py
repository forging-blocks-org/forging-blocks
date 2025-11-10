#!/usr/bin/env python3
"""Automatic class member reordering script for BuildingBlocks."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

import libcst as cst

ORDER_PRIORITY = [
    "__new__",
    "__init__",
    "classmethod",
    "staticmethod",
    "property",
    "method",
    "dunder",
    "other",
]


def has_decorator(fn: cst.FunctionDef, name: str) -> bool:
    """Return True if the function has a decorator with the given name."""
    for dec in fn.decorators or []:
        expr = dec.decorator
        if isinstance(expr, cst.Name) and expr.value == name:
            return True
        if isinstance(expr, cst.Attribute) and expr.attr.value == name:
            return True
    return False


def is_docstring_stmt(stmt: cst.CSTNode) -> bool:
    """Return True if the statement is a docstring (bare string literal)."""
    if not isinstance(stmt, cst.SimpleStatementLine):
        return False
    if len(stmt.body) != 1 or not isinstance(stmt.body[0], cst.Expr):
        return False
    return isinstance(stmt.body[0].value, (cst.SimpleString, cst.ConcatenatedString))


def classify_member(node: cst.CSTNode, index: int) -> tuple[int, int]:
    """Return a sort key for ordering within a class."""
    if is_docstring_stmt(node):
        return (-1, 0)  # ensure it stays first

    if not isinstance(node, cst.FunctionDef):
        return ORDER_PRIORITY.index("other"), index

    name = node.name.value
    if name == "__new__":
        return ORDER_PRIORITY.index("__new__"), index
    if name == "__init__":
        return ORDER_PRIORITY.index("__init__"), index
    if has_decorator(node, "classmethod"):
        return ORDER_PRIORITY.index("classmethod"), index
    if has_decorator(node, "staticmethod"):
        return ORDER_PRIORITY.index("staticmethod"), index
    if has_decorator(node, "property"):
        return ORDER_PRIORITY.index("property"), index
    if name.startswith("__") and name.endswith("__"):
        return ORDER_PRIORITY.index("dunder"), index
    return ORDER_PRIORITY.index("method"), index


class ReorderClassMembers(cst.CSTTransformer):
    """Transformer that reorders class body elements."""

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:
        """Reorder members within a class definition."""
        body_items = list(updated_node.body.body)
        if not body_items:
            return updated_node

        # Separate and preserve leading docstring (if present)
        docstring_stmt = None
        if is_docstring_stmt(body_items[0]):
            docstring_stmt = body_items.pop(0)

        # Sort remaining members
        reordered = sorted(
            enumerate(body_items),
            key=lambda pair: classify_member(pair[1], pair[0]),
        )
        new_body = [stmt for _, stmt in reordered]

        # Re-insert preserved docstring at top
        if docstring_stmt is not None:
            new_body.insert(0, docstring_stmt)

        return updated_node.with_changes(body=updated_node.body.with_changes(body=new_body))


def reorder_file(path: Path) -> bool:
    """Reorder class members in the given Python file."""
    try:
        src = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[WARN] Could not read {path}: {e}")
        return False

    try:
        tree = cst.parse_module(src)
    except Exception as e:
        print(f"[WARN] Parse error in {path}: {e}")
        return False

    new_tree = tree.visit(ReorderClassMembers())
    if new_tree.code != src:
        path.write_text(new_tree.code, encoding="utf-8")
        print(f"[FIXED] {path}")
        return True
    return False


def main(argv: Sequence[str]) -> int:
    """Main entry point for the script."""
    paths: list[Path] = []
    if argv:
        for arg in argv:
            p = Path(arg)
            if p.is_dir():
                paths.extend(p.rglob("*.py"))
            elif p.suffix == ".py":
                paths.append(p)
    else:
        paths.extend(Path("src").rglob("*.py"))
        paths.extend(Path("tests").rglob("*.py"))

    modified = sum(reorder_file(p) for p in paths)
    print(f"Reordered {modified} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
