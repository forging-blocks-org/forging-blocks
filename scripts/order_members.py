#!/usr/bin/env python3
"""Reorder Python class members according to Google Python Style Guide.

This script automatically reorders class members to follow a consistent order:
1. Class docstring
2. Class constants (CAPS_WITH_UNDER)
3. Public class variables (lower_with_under)
4. Protected class variables (_lower_with_under)
5. Private class variables (__lower_with_under)
6. __new__ method
7. __init__ method
8. Other magic methods (__repr__, __str__, __eq__, etc.)
9. Properties (@property, with getters/setters together)
10. Class methods (@classmethod)
11. Static methods (@staticmethod)
12. Public methods
13. Protected methods (_method)
14. Private methods (__method)

Usage:
    python order_members.py [paths...]

    If no paths provided, processes all .py files in src/ and tests/
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

import libcst as cst

# Order priority based on Google Python Style Guide conventions
ORDER_PRIORITY = [
    "docstring",  # 1. Class docstring
    "class_constant",  # 2. Class constants (CAPS_WITH_UNDER)
    "class_variable",  # 3. Public class variables
    "protected_class_var",  # 4. Protected class variables (_var)
    "private_class_var",  # 5. Private class variables (__var)
    "__new__",  # 6. __new__ constructor
    "__init__",  # 7. __init__ constructor
    "dunder",  # 8. Other magic methods
    "property",  # 9. Properties
    "classmethod",  # 10. Class methods
    "staticmethod",  # 11. Static methods
    "public_method",  # 12. Public methods
    "protected_method",  # 13. Protected methods (_method)
    "private_method",  # 14. Private methods (__method)
    "other",  # 15. Other statements
]


def has_decorator(fn: cst.FunctionDef, name: str) -> bool:
    """Check if function has a specific decorator.

    Args:
        fn: The function definition to check.
        name: The decorator name to look for.

    Returns:
        True if the decorator is present, False otherwise.
    """
    for dec in fn.decorators or []:
        expr = dec.decorator
        if isinstance(expr, cst.Name) and expr.value == name:
            return True
        if isinstance(expr, cst.Attribute) and expr.attr.value == name:
            return True
    return False


def is_docstring_stmt(stmt: cst.CSTNode) -> bool:
    """Check if statement is a docstring.

    Args:
        stmt: The statement to check.

    Returns:
        True if the statement is a docstring, False otherwise.
    """
    if not isinstance(stmt, cst.SimpleStatementLine):
        return False
    if len(stmt.body) != 1 or not isinstance(stmt.body[0], cst.Expr):
        return False
    return isinstance(stmt.body[0].value, (cst.SimpleString, cst.ConcatenatedString))


def get_attribute_name(stmt: cst.CSTNode) -> str | None:
    """Get the attribute name from an assignment statement.

    Args:
        stmt: The statement to check.

    Returns:
        The attribute name if it's an assignment, None otherwise.
    """
    if not isinstance(stmt, cst.SimpleStatementLine):
        return None

    for sub in stmt.body:
        # Handle annotated assignments: var: Type = value
        if isinstance(sub, cst.AnnAssign) and isinstance(sub.target, cst.Name):
            return sub.target.value

        # Handle regular assignments: var = value
        if isinstance(sub, cst.Assign):
            for target in sub.targets:
                if isinstance(target.target, cst.Name):
                    return target.target.value

    return None


def classify_attribute(name: str) -> str:
    """Classify attribute by naming convention.

    Args:
        name: The attribute name.

    Returns:
        The attribute classification.
    """
    # Class constants: CAPS_WITH_UNDER (must be all uppercase and contain an underscore, or be
    # longer than one character)
    if name.isupper() and (len(name) > 1 or "_" in name):
        return "class_constant"

    # Private class variables: __var (but not __dunder__)
    if name.startswith("__") and not name.endswith("__"):
        return "private_class_var"

    # Protected class variables: _var
    if name.startswith("_"):
        return "protected_class_var"

    # Public class variables
    return "class_variable"


def classify_member(node: cst.CSTNode, index: int) -> tuple[int, int]:
    """Classify class member for ordering according to Google Style Guide.

    Args:
        node: The class member node to classify.
        index: The original index of the member (for stable sorting).

    Returns:
        A tuple of (priority, original_index) for sorting.
    """
    # Docstring must be first
    if is_docstring_stmt(node):
        return ORDER_PRIORITY.index("docstring"), index

    # Class attributes (constants, variables)
    attr_name = get_attribute_name(node)
    if attr_name:
        attr_type = classify_attribute(attr_name)
        return ORDER_PRIORITY.index(attr_type), index

    # Non-function members
    if not isinstance(node, cst.FunctionDef):
        return ORDER_PRIORITY.index("other"), index

    name = node.name.value

    # Constructors
    if name == "__new__":
        return ORDER_PRIORITY.index("__new__"), index
    if name == "__init__":
        return ORDER_PRIORITY.index("__init__"), index

    # Properties (before classmethods/staticmethods per Google guide)
    if has_decorator(node, "property"):
        return ORDER_PRIORITY.index("property"), index

    # Other magic methods (after __init__, before properties)
    if name.startswith("__") and name.endswith("__"):
        return ORDER_PRIORITY.index("dunder"), index

    # Class methods
    if has_decorator(node, "classmethod"):
        return ORDER_PRIORITY.index("classmethod"), index

    # Static methods
    if has_decorator(node, "staticmethod"):
        return ORDER_PRIORITY.index("staticmethod"), index

    # Private methods (double underscore)
    # Note: Actual private methods use name mangling (__method -> _ClassName__method)
    # But we check the declared name
    if name.startswith("__") and not name.endswith("__"):
        return ORDER_PRIORITY.index("private_method"), index

    # Protected methods (single underscore)
    if name.startswith("_"):
        return ORDER_PRIORITY.index("protected_method"), index

    # Public methods
    return ORDER_PRIORITY.index("public_method"), index


class ReorderClassMembers(cst.CSTTransformer):
    """Reorder class members according to Google Python Style Guide."""

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:
        """Reorder members of a class definition.

        Args:
            original_node: The original class definition.
            updated_node: The updated class definition.

        Returns:
            The class definition with reordered members.
        """
        body_items = list(updated_node.body.body)
        if not body_items:
            return updated_node

        # Sort by priority, maintaining original order for same priority (stable sort)
        reordered = sorted(
            enumerate(body_items),
            key=lambda pair: classify_member(pair[1], pair[0]),
        )

        new_body = [stmt for _, stmt in reordered]
        return updated_node.with_changes(body=updated_node.body.with_changes(body=new_body))


def reorder_file(path: Path) -> bool:
    """Reorder class members in a single Python file.

    Args:
        path: Path to the Python file to process.

    Returns:
        True if the file was modified, False otherwise.
    """
    try:
        src = path.read_text(encoding="utf-8")
    except Exception:
        return False

    try:
        tree = cst.parse_module(src)
    except Exception:
        return False

    new_tree = tree.visit(ReorderClassMembers())

    if new_tree.code != src:
        path.write_text(new_tree.code, encoding="utf-8")
        print(f"[FIXED] {path}")
        return True

    return False


def main(argv: Sequence[str]) -> int:
    """Reorder class members in Python files.

    Args:
        argv: Command-line arguments (file or directory paths).

    Returns:
        Exit code (0 for success).
    """
    paths: list[Path] = []

    if argv:
        for arg in argv:
            p = Path(arg)
            if p.is_dir():
                paths.extend(p.rglob("*.py"))
            elif p.suffix == ".py":
                paths.append(p)
    else:
        # Default: process src/ and tests/ directories
        paths.extend(Path("src").rglob("*.py"))
        paths.extend(Path("tests").rglob("*.py"))

    modified = sum(reorder_file(p) for p in paths)
    print(f"Reordered {modified} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
