"""
API Reference generator for ForgingBlocks.

This script generates API-level documentation from docstrings.
It is intended for contributors and advanced users, not as a replacement
for curated Guide or Reference documentation.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

SRC_DIR = Path("src/forging_blocks")
OUT_DIR = Path("docs/reference/autodoc")
MKDOCS_YML = Path("mkdocs.yml")


def read_docstring(file: Path) -> str:
    """Read the top-level docstring from a Python file."""
    try:
        source = file.read_text(encoding="utf-8")
        tree = ast.parse(source)
        return ast.get_docstring(tree) or ""
    except Exception as e:
        print(f"⚠️ Failed reading {file}: {e}")
        return ""


def module_title(path: Path) -> str:
    """Convert a module path to a readable title."""
    return path.stem.replace("_", " ").title()


def import_path(path: Path) -> str:
    """Convert a file path to a Python import path."""
    rel = path.relative_to(SRC_DIR)
    return f"forging_blocks.{'.'.join(rel.with_suffix('').parts)}"


def ensure_dir(path: Path) -> None:
    """Ensure the parent directory of a path exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def find_source_files(base: Path) -> list[Path]:
    """Find all Python source files, excluding __init__.py."""
    return [p for p in base.rglob("*.py") if p.name != "__init__.py"]


def generate_markdown(src: Path) -> Path:
    """Generate a markdown file for a given Python source file."""
    title = module_title(src)
    doc = read_docstring(src)
    out = OUT_DIR / src.relative_to(SRC_DIR).with_suffix(".md")
    ensure_dir(out)

    content = [f"# {title}", ""]
    if doc:
        content.append(doc)
        content.append("")

    content += [
        f"::: {import_path(src)}",
        "    options:",
        "      show_source: true",
        "      show_root_heading: true",
    ]
    out.write_text("\n".join(content), encoding="utf-8")

    print(f"✅ Generated: {out}")
    return out


def build_autodoc_section(files: list[Path], indent: str = "      ") -> str:
    """Build the MkDocs navigation section for autodoc pages."""
    grouped: dict[str, dict[str | None, list[tuple[str, str]]]] = {}

    for file in files:
        parts = file.relative_to(OUT_DIR).parts
        if len(parts) < 1:
            continue

        # Top-level layer (e.g., "application", "domain", "foundation")
        layer = parts[0].capitalize()

        # Determine sublayer and title
        if len(parts) == 2:
            # Direct file under layer: foundation/result.md
            sublayer = None
            title = parts[1].removesuffix(".md").replace("_", " ").title()
        else:
            # Nested file: application/ports/inbound/use_case.md
            # Sublayer: "Ports" (parts[1])
            sublayer_parts = parts[1:-1]
            sublayer = " / ".join(p.replace("_", " ").title() for p in sublayer_parts)
            title = parts[-1].removesuffix(".md").replace("_", " ").title()

        path = f"reference/autodoc/{'/'.join(parts)}"
        grouped.setdefault(layer, {}).setdefault(sublayer, []).append((title, path))

    # Generate navigation
    lines = [f"{indent}- API Reference:"]
    for layer, subgroups in sorted(grouped.items()):
        lines.append(f"{indent}  - {layer}:")

        # Sort: None (direct) first, then alphabetically
        for sublayer, entries in sorted(
            subgroups.items(), key=lambda x: ("" if x[0] is None else x[0])
        ):
            if sublayer is None:
                # Direct entries
                for name, link in sorted(entries):
                    lines.append(f"{indent}    - {name}: {link}")
            else:
                # Nested sublayers
                lines.append(f"{indent}    - {sublayer}:")
                for name, link in sorted(entries):
                    lines.append(f"{indent}      - {name}: {link}")

    return "\n".join(lines)


def update_nav(mkdocs: str, section: str) -> str:
    """Update the MkDocs navigation section with the autodoc section."""
    # Try to find and replace existing API Reference section
    pattern = (
        r"(?ms)^      - API Reference:.*?(?=^      - [A-Z]|^  - [A-Z]|^[a-z_]+:|\Z)"
    )
    if re.search(pattern, mkdocs):
        return re.sub(pattern, section + "\n", mkdocs)

    # Insert after Reference section
    ref_pattern = r"(^  - Reference:\n(?:^      - .*\n)*)"
    match = re.search(ref_pattern, mkdocs, re.MULTILINE)
    if match:
        insert_pos = match.end()
        return mkdocs[:insert_pos] + section + "\n" + mkdocs[insert_pos:]

    # Fallback: add at the end
    return mkdocs.rstrip() + "\n" + section + "\n"


def ensure_autodoc_index(out_dir: Path) -> None:
    index_file = out_dir / "index.md"

    if index_file.exists():
        return

    index_file.write_text(
        """# API Reference

!!! note "About this section"
    This section is generated automatically from code docstrings.
    It documents the public API surface of ForgingBlocks.

    For architectural intent, design rationale, and usage guidance,
    refer to the hand-written **Guide** and **Reference** sections.
""",
        encoding="utf-8",
    )


def main() -> None:
    """Main function to generate autodoc pages and update mkdocs.yml."""
    if not SRC_DIR.exists():
        print(f"❌ Source directory not found: {SRC_DIR}")
        sys.exit(1)

    files = [generate_markdown(p) for p in find_source_files(SRC_DIR)]

    mkdocs_text = MKDOCS_YML.read_text(encoding="utf-8")
    section = build_autodoc_section(files)
    updated_mkdocs = update_nav(mkdocs_text, section)
    MKDOCS_YML.write_text(updated_mkdocs, encoding="utf-8")

    print("\n📘 Autodoc generation complete.\n")


if __name__ == "__main__":
    main()
