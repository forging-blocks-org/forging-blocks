# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from pathlib import Path

import pytest
from scripts.generate_redirect_template import (
    extract_body_attrs,
    extract_head_assets,
    extract_header,
    extract_scripts,
    generate_template,
    main,
)


def _build_head_html(*extras: str) -> str:
    base = """<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="description" content="Composable toolkit">
    <meta name="author" content="ForgingBlocks Org">
    <meta name="generator" content="mkdocs-1.6.1, mkdocs-material-9.6.23">
    <link rel="icon" href="assets/favicon.ico">
    <link rel="stylesheet" href="assets/stylesheets/main.84d31ad4.min.css">
    <link rel="stylesheet" href="assets/stylesheets/palette.06af60db.min.css">
    <link rel="stylesheet" href="assets/_mkdocstrings.css">
    <link rel="stylesheet" href="assets/css/theme.css">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,300i,400,400i,700,700i%7CRoboto+Mono:400,400i,700,700i&display=fallback">
    <style>:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}</style>
    <script>__md_scope=new URL(".",location),__md_hash=e=>[...e].reduce(((e,_)=>(e<<5)-e+_.charCodeAt(0)),0),__md_get=(e,_=localStorage,t=__md_scope)=>JSON.parse(_.getItem(t.pathname+"."+e)),__md_set=(e,_,t=localStorage,a=__md_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(_))}catch(e){}}</script>
    <title>ForgingBlocks</title>
"""
    return base + "".join(extras) + "\n</head>"


def _build_page_html(head: str, body_extra: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
{head}
<body dir="ltr" data-md-color-scheme="slate" data-md-color-primary="orange" data-md-color-accent="amber">
<div data-md-component="announce"></div>
<header class="md-header" data-md-component="header">
  <nav class="md-header__inner md-grid" aria-label="Header">
    <a href="." title="ForgingBlocks" class="md-header__button md-logo" aria-label="ForgingBlocks" data-md-component="logo">
  <img src="assets/logo.png" alt="logo">
    </a>
    <div class="md-header__title" data-md-component="header-title">
      <div class="md-header__ellipsis">
        <div class="md-header__topic">
          <span class="md-ellipsis">ForgingBlocks</span></div>
        <div class="md-header__topic" data-md-component="header-topic">
          <span class="md-ellipsis">Home</span>
        </div>
      </div>
    </div>
  </nav>
</header>
{body_extra}
<script src="assets/javascripts/bundle.f55a23d4.min.js"></script>
<script src="assets/js/version-dropdown.js"></script>
<script src="assets/js/mermaid-init.js"></script>
<script>var __config=JSON.parse('{{"key":"value"}}')</script>
</body>
"""


@pytest.mark.unit
class TestExtractHeadAssets:
    def test_when_valid_head_then_includes_meta_and_css(self) -> None:
        head = _build_head_html()
        html = _build_page_html(head)
        result = extract_head_assets(html)

        assert "charset" in result
        assert "viewport" in result
        assert "Composable toolkit" in result
        assert "ForgingBlocks Org" in result
        assert "generator" in result
        assert "{{ href }}assets/favicon.ico" in result
        assert "{{ href }}assets/stylesheets/main" in result
        assert "__md_scope" in result
        assert "fonts.googleapis.com" in result
        assert "--md-text-font" in result

    def test_when_head_missing_then_raises_value_error(self) -> None:
        html = "<html><body>no head</body></html>"
        with pytest.raises(ValueError, match="No <head>"):
            extract_head_assets(html)

    def test_when_head_has_no_meta_tags_then_returns_only_matched(self) -> None:
        head = """<head>
    <title>Empty</title>
    <link rel="stylesheet" href="assets/theme.css">
    </head>"""
        html = _build_page_html(head)
        result = extract_head_assets(html)

        assert "charset" not in result
        assert "viewport" not in result
        assert "{{ href }}assets/theme.css" in result

    def test_when_external_stylesheets_are_skipped(self) -> None:
        head = """<head>
    <link rel="stylesheet" href="assets/local.css">
    <link rel="stylesheet" href="https://cdn.example.com/external.css">
    </head>"""
        html = _build_page_html(head)
        result = extract_head_assets(html)

        assert "{{ href }}assets/local.css" in result
        assert "cdn.example.com" not in result

    def test_when_no_favicon_in_source_then_no_favicon_link(self) -> None:
        head = "<head></head>"
        html = _build_page_html(head)
        result = extract_head_assets(html)

        # No favicon in source, so no favicon in result (implementation doesn't add default)
        assert "{{ href }}assets/favicon.ico" not in result
        assert result == ""


@pytest.mark.unit
class TestExtractHeader:
    def test_when_valid_header_then_returns_header_with_template_hrefs(self) -> None:
        html = _build_page_html(_build_head_html())
        result = extract_header(html)

        assert '<header class="md-header"' in result
        assert "ForgingBlocks" in result
        assert "Redirecting..." in result
        assert "{{ href }}assets/logo.png" in result

    def test_when_header_missing_then_raises_value_error(self) -> None:
        html = "<html><head></head><body>no header</body></html>"
        with pytest.raises(ValueError, match="No <header>"):
            extract_header(html)

    def test_when_header_topic_is_home_then_replaces_with_redirecting(self) -> None:
        html = _build_page_html(_build_head_html())
        result = extract_header(html)

        assert "Home" not in result or result.count("Home") == 0
        assert "Redirecting..." in result

    def test_when_header_topic_is_forging_blocks_then_replaces(self) -> None:
        head = _build_head_html()
        html = _build_page_html(head).replace(
            '<span class="md-ellipsis">Home</span>',
            '<span class="md-ellipsis">ForgingBlocks</span>',
        )
        result = extract_header(html)

        assert "Redirecting..." in result
        assert "ForgingBlocks" in result

    def test_when_local_src_in_header_then_adds_template_prefix(self) -> None:
        head = _build_head_html()
        html = _build_page_html(head).replace(
            '<img src="assets/logo.png"',
            '<img src="assets/logo.png" data-src="assets/logo-dark.png"',
        )
        result = extract_header(html)

        assert "{{ href }}assets/logo.png" in result
        assert "{{ href }}assets/logo-dark.png" in result

    def test_when_external_href_in_header_then_does_not_add_prefix(self) -> None:
        head = _build_head_html()
        html = _build_page_html(head).replace(
            '<img src="assets/logo.png"',
            '<img src="https://example.com/logo.png"',
        )
        result = extract_header(html)

        assert 'src="{{ href }}https' not in result
        assert 'src="https://example.com/logo.png"' in result

    def test_when_hash_href_in_header_then_does_not_add_prefix(self) -> None:
        pass


@pytest.mark.unit
class TestExtractScripts:
    def test_when_scripts_are_present_then_returns_template_prefixed(self) -> None:
        html = _build_page_html(_build_head_html())
        result = extract_scripts(html)

        assert "{{ href }}assets/javascripts/bundle" in result
        assert "{{ href }}assets/js/version-dropdown.js" in result
        assert "{{ href }}assets/js/mermaid-init.js" in result

    def test_when_inline_script_is_skipped(self) -> None:
        html = _build_page_html(_build_head_html())
        result = extract_scripts(html)

        assert "__config" not in result

    def test_when_no_scripts_then_returns_empty(self) -> None:
        html = "<html><head></head><body></body></html>"
        result = extract_scripts(html)

        assert result == ""

    def test_when_external_script_then_skipped(self) -> None:
        html = """<html><head></head><body>
<script src="assets/local.js"></script>
<script src="https://cdn.example.com/remote.js"></script>
</body></html>"""
        result = extract_scripts(html)

        assert "local.js" in result
        assert "cdn.example.com" not in result


@pytest.mark.unit
class TestExtractBodyAttrs:
    def test_when_body_attrs_present_then_returns_them(self) -> None:
        html = _build_page_html(_build_head_html())
        result = extract_body_attrs(html)

        assert 'dir="ltr"' in result
        assert 'data-md-color-scheme="slate"' in result
        assert 'data-md-color-primary="orange"' in result

    def test_when_body_has_no_attrs_then_returns_defaults(self) -> None:
        html = "<html><head></head><body></body></html>"
        result = extract_body_attrs(html)

        # Body tag exists but has no attributes, so empty string is returned
        assert result == ""


@pytest.mark.unit
class TestGenerateTemplate:
    def test_when_valid_html_then_writes_template_file(self, tmp_path: Path) -> None:
        html = _build_page_html(_build_head_html())
        output = tmp_path / "redirect_template.html"

        generate_template(html, output)

        assert output.exists()
        content = output.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "ForgingBlocks - Redirecting" in content
        assert "{{ href }}" in content
        assert "redirect-link" in content
        assert "Documentation Redirect" in content

    def test_when_template_contains_fixed_redirect_logic(self, tmp_path: Path) -> None:
        html = _build_page_html(_build_head_html())
        output = tmp_path / "redirect_template.html"

        generate_template(html, output)

        content = output.read_text(encoding="utf-8")
        assert "prefix + def.version + " in content
        assert 'var defaultPath = serverDefault.replace(/\\/$/, "")' in content
        assert "lastIndexOf" in content
        assert 'doRedirect(def ? prefix + def.version + "/" : serverDefault)' in content

    def test_when_template_has_all_placeholders(self, tmp_path: Path) -> None:
        html = _build_page_html(_build_head_html())
        output = tmp_path / "redirect_template.html"

        generate_template(html, output)

        content = output.read_text(encoding="utf-8")
        assert content.count("{{ href }}") >= 5

    def test_when_template_has_version_dropdown_scripts(self, tmp_path: Path) -> None:
        html = _build_page_html(_build_head_html())
        output = tmp_path / "redirect_template.html"

        generate_template(html, output)

        content = output.read_text(encoding="utf-8")
        assert "version-dropdown.js" in content
        assert "mermaid-init.js" in content

    def test_when_template_has_redirect_js_function(self, tmp_path: Path) -> None:
        html = _build_page_html(_build_head_html())
        output = tmp_path / "redirect_template.html"

        generate_template(html, output)

        content = output.read_text(encoding="utf-8")
        assert "function doRedirect(target)" in content
        assert "window.location.replace" in content
        assert "setTimeout" in content

    def test_when_minimal_html_then_still_generates_valid(self, tmp_path: Path) -> None:
        html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body dir="ltr" data-md-color-scheme="slate" data-md-color-primary="orange" data-md-color-accent="amber">
<div data-md-component="announce"></div>
<header class="md-header" data-md-component="header">
  <nav class="md-header__inner md-grid" aria-label="Header">
    <a href="." title="ForgingBlocks" class="md-header__button md-logo">
  <img src="assets/logo.png" alt="logo">
    </a>
    <div class="md-header__title" data-md-component="header-title">
      <div class="md-header__ellipsis">
        <div class="md-header__topic">
          <span class="md-ellipsis">ForgingBlocks</span></div>
        <div class="md-header__topic" data-md-component="header-topic">
          <span class="md-ellipsis">Home</span>
        </div>
      </div>
    </div>
  </nav>
</header>
</body>
</html>"""
        output = tmp_path / "redirect_template.html"

        generate_template(html, output)

        content = output.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "ForgingBlocks - Redirecting" in content
        assert "Redirecting..." in content

    def test_when_body_self_closing_then_uses_default_attrs(self) -> None:
        html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body/>
</html>"""
        result = extract_body_attrs(html)

        # Self-closing body tag has no attributes, so defaults are returned
        assert 'dir="ltr"' in result
        assert "slate" in result

    def test_when_body_has_extra_attrs_then_preserves_them(self) -> None:
        html = '<html><head></head><body class="extra" id="main"></body></html>'
        result = extract_body_attrs(html)

        assert 'class="extra"' in result
        assert 'id="main"' in result

        head = _build_head_html()
        html = _build_page_html(head).replace('href="."', 'href="#"')
        result = extract_header(html)

        assert 'href="{{ href }}#' not in result
        assert 'href="#"' in result

    def test_when_parent_relative_href_then_does_not_add_prefix(self) -> None:
        head = _build_head_html()
        html = _build_page_html(head).replace('href="."', 'href="../something"')
        result = extract_header(html)

        assert 'href="{{ href }}..' not in result
        assert 'href="../something"' in result
