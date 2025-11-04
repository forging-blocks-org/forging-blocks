# scripts/gen_ref_pages.py
"""Auto-generate placeholder pages for the reference section.

This prevents mkdocs-gen-files from failing when no generation logic exists yet.
You can later expand this to dynamically scan your src/ directory.
"""
from pathlib import Path

import mkdocs_gen_files

# Create reference/index.md dynamically
path = Path("reference/index.md")
with mkdocs_gen_files.open(path, "w") as f:
    f.write(
        "# API Reference\n\n"
        "This section contains the API documentation generated from docstrings.\n\n"
        "Each submodule page is automatically built using `mkdocstrings`.\n"
    )

# Optionally set the edit path for 'Edit on GitHub' links
# mkdocs_gen_files.set_edit_path(path, "scripts/gen_ref_pages.py")
