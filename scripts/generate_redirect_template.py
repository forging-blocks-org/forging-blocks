"""Generate the redirect template for mike set-default.

This script reads a built MkDocs page and extracts the Material theme
assets (CSS, JS, fonts, header structure) to create a redirect template
that looks identical to the main documentation pages.

The template uses Jinja2 `{{ href }}` placeholders that mike replaces
at set-default time with the version path (e.g., `dev/`).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def extract_head_assets(html: str) -> str:
    """Extract CSS, font, and meta elements from <head>."""
    head_match = re.search(r"<head>(.*?)</head>", html, re.DOTALL)
    if not head_match:
        raise ValueError("No <head> found in HTML")
    
    head_content = head_match.group(1)
    
    # Extract individual elements we want to keep
    parts = []
    
    # Meta charset and viewport
    for tag in ["<meta charset", '<meta name="viewport"',
                '<meta name="description"', '<meta name="author"']:
        m = re.search(rf"({re.escape(tag)}[^>]*>)", head_content)
        if m:
            parts.append(m.group(1))
    
    # Generator
    m = re.search(r"(<meta name=\"generator\"[^>]*>)", head_content)
    if m:
        parts.append(m.group(1))
    
    # Title (we override this)
    # Favicon
    m = re.search(r"(<link rel=\"icon\"[^>]*>)", head_content)
    if m:
        parts.append(f'<link rel="icon" href="{{{{ href }}}}assets/favicon.ico">')
    
    # Remove canonical and next links
    
    # CSS stylesheets (keep all local ones, skip external)
    for m in re.finditer(
        r'<link rel="stylesheet" href="(?!https?://)([^"]+)"', head_content
    ):
        href = m.group(1)
        # Skip mkdocstrings CSS if it causes issues (usually fine)
        parts.append(f'<link rel="stylesheet" href="{{{{ href }}}}{href}">')
    
    # Google Fonts and preconnect (keep as-is, they're external)
    for m in re.finditer(
        r'<link[^>]*fonts\.[^>]*>', head_content
    ):
        parts.append(m.group(0))
    
    # Inline style for fonts
    m = re.search(r"<style>:root\{[^}]*--md-text-font[^<]*</style>", head_content)
    if m:
        parts.append(m.group(0))
    
    # MkDocs Material JS scope setup
    m = re.search(r"<script>__md_scope.*?</script>", head_content, re.DOTALL)
    if m:
        parts.append(m.group(0))
    
    return "\n    ".join(parts)


def extract_header(html: str) -> str:
    """Extract the Material theme header/nav."""
    header_match = re.search(
        r"(<header class=.md-header[^>]*>.*?</header>)", html, re.DOTALL
    )
    if not header_match:
        raise ValueError("No <header> found in HTML")
    
    header = header_match.group(1)
    
    # Fix the header topic to show "Redirecting..." instead of "Home"
    header = re.sub(
        r'(<span class="md-ellipsis">)\s*(Home|ForgingBlocks)\s*(</span>)\s*'
        r'(</div>\s*<div class="md-header__topic"[^>]*>\s*<span class="md-ellipsis">)\s*[^<]*\s*',
        r'\1ForgingBlocks\3\4Redirecting...',
        header,
        flags=re.DOTALL,
    )
    
    # Add {{ href }} prefix to local asset references
    header = re.sub(
        r'(src|href)="(?!https?://|#|\.\./)([^"]+)"',
        r'\1="{{ href }}\2"',
        header,
    )
    
    # Fix the home link: if it's just "." keep it as "." (it stays on root)
    # but other relative links should get the {{ href }} prefix
    # Actually we want all local assets to point to the version directory
    
    return header


def extract_scripts(html: str) -> str:
    """Extract JS scripts from the page."""
    scripts = []
    for m in re.finditer(
        r'<script src="(?!https?://)(assets/[^"]+)"[^>]*></script>', html
    ):
        scripts.append(f'<script src="{{{{ href }}}}{m.group(1)}"></script>')
    
    # Also add the search/translations inline script
    trans_match = re.search(
        r'(<script id="__config"[^>]*>.*?</script>)', html, re.DOTALL
    )
    # Skip __config - it's too complex and not needed for redirect page
    
    return "\n    ".join(scripts)


def extract_body_attrs(html: str) -> str:
    """Extract body tag attributes."""
    m = re.search(r"<body([^>]*)>", html)
    if m:
        return m.group(1).strip()
    return 'dir="ltr" data-md-color-scheme="slate" data-md-color-primary="orange" data-md-color-accent="amber"'


def generate_template(source_html: str, output_path: Path) -> None:
    """Generate the redirect template from a built MkDocs page."""
    head_assets = extract_head_assets(source_html)
    header = extract_header(source_html)
    scripts = extract_scripts(source_html)
    body_attrs = extract_body_attrs(source_html)
    
    template = f'''<!DOCTYPE html>
<html lang="en" class="no-js">
  <head>
    {head_assets}
    <title>ForgingBlocks - Redirecting</title>
  </head>
  <body {body_attrs}>
    <div data-md-component="announce"></div>
    {header}
    <div class="md-container" data-md-component="container">
      <main class="md-main" data-md-component="main">
        <div class="md-main__inner md-grid">
          <div class="md-content" data-md-component="content">
            <article class="md-content__inner md-typeset">
              <h1>Documentation Redirect</h1>
              <p>
                If you are not redirected automatically,
                <a id="redirect-link" href="#">click here</a>.
              </p>
              <p style="margin-top: 1rem; opacity: 0.6;">
                You can also select a specific version from the
                dropdown in the bottom-right corner.
              </p>
            </article>
          </div>
        </div>
      </main>
    </div>
    {scripts}
    <script>
      (function() {{
        var serverDefault = "{{{{ href }}}}";
        var linkEl = document.getElementById("redirect-link");
        if (linkEl) linkEl.href = serverDefault;

        var versionsUrl = "{{{{ href }}}}versions.json";
        var timer = null;

        function doRedirect(target) {{
          if (linkEl) linkEl.href = target;
          if (timer) clearTimeout(timer);
          timer = setTimeout(function() {{
            window.location.replace(
              target + window.location.search + window.location.hash
            );
          }}, 3000);
        }}

        fetch(versionsUrl)
          .then(function(r) {{ return r.ok ? r.json() : Promise.reject(r); }})
          .then(function(versions) {{
            var def = null;
            for (var i = 0; i < versions.length; i++) {{
              if (versions[i].is_default) {{ def = versions[i]; break; }}
            }}
            if (!def && versions.length > 0) def = versions[0];
            doRedirect(def ? def.version + "/" : serverDefault);
          }})
          .catch(function() {{ doRedirect(serverDefault); }});
      }})();
    </script>
  </body>
</html>
'''
    
    output_path.write_text(template, encoding="utf-8")
    print(f"✅ Generated redirect template: {output_path}")


def main() -> int:
    """Main entry point."""
    # Default paths
    site_dir = Path("site")
    output = Path("docs/redirect_template.html")
    
    # Allow overriding via args
    if len(sys.argv) >= 2:
        site_dir = Path(sys.argv[1])
    if len(sys.argv) >= 3:
        output = Path(sys.argv[2])
    
    index_html = site_dir / "index.html"
    if not index_html.exists():
        print(f"❌ Built site not found at: {index_html}")
        print(f"   Run 'mkdocs build' first, then re-run this script.")
        return 1
    
    source_html = index_html.read_text(encoding="utf-8")
    generate_template(source_html, output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
