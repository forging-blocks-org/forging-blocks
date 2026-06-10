# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from pathlib import Path

import pytest
from scripts.generate_autodoc_pages import (
    OUT_DIR,
    SRC_DIR,
    build_autodoc_section,
    ensure_autodoc_index,
    ensure_dir,
    find_source_files,
    generate_markdown,
    import_path,
    main,
    module_title,
    update_nav,
)


@pytest.mark.unit
class TestModuleTitle:
    def test_when_simple_name_then_returns_title(self) -> None:
        path = Path("result.py")

        result = module_title(path)

        assert result == "Result"

    def test_when_underscore_name_then_converts_to_title(self) -> None:
        path = Path("my_module.py")

        result = module_title(path)

        assert result == "My Module"

    def test_when_multi_level_path_then_uses_stem_only(self) -> None:
        path = Path("domain/value_objects.py")

        result = module_title(path)

        assert result == "Value Objects"


@pytest.mark.unit
class TestImportPath:
    def test_when_simple_path_then_returns_dotted_import(self) -> None:
        path = SRC_DIR / "result.py"

        result = import_path(path)

        assert result == "forging_blocks.result"

    def test_when_nested_path_then_returns_dotted_import(self) -> None:
        path = SRC_DIR / "domain" / "value_objects.py"

        result = import_path(path)

        assert result == "forging_blocks.domain.value_objects"


@pytest.mark.unit
class TestEnsureDir:
    def test_when_parent_does_not_exist_then_creates_it(self, tmp_path: Path) -> None:
        target = tmp_path / "sub" / "file.md"

        ensure_dir(target)

        assert target.parent.exists()

    def test_when_parent_exists_then_does_not_raise(self, tmp_path: Path) -> None:
        target = tmp_path / "file.md"

        ensure_dir(target)

        assert target.parent.exists()


@pytest.mark.unit
class TestFindSourceFiles:
    def test_when_directory_then_returns_py_files_excluding_init(
        self, tmp_path: Path
    ) -> None:
        (tmp_path / "module.py").write_text("")
        (tmp_path / "__init__.py").write_text("")
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "nested.py").write_text("")
        (tmp_path / "sub" / "__init__.py").write_text("")

        result = find_source_files(tmp_path)

        assert sorted(p.name for p in result) == ["module.py", "nested.py"]

    def test_when_empty_directory_then_returns_empty(self, tmp_path: Path) -> None:
        result = find_source_files(tmp_path)

        assert result == []

    def test_when_only_init_files_then_returns_empty(self, tmp_path: Path) -> None:
        (tmp_path / "__init__.py").write_text("")

        result = find_source_files(tmp_path)

        assert result == []


@pytest.mark.unit
class TestGenerateMarkdown:
    def test_when_source_with_docstring_then_creates_markdown(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        src_dir = tmp_path / "src" / "forging_blocks"
        out_dir = tmp_path / "docs" / "reference" / "autodoc"
        src_dir.mkdir(parents=True)
        out_dir.mkdir(parents=True)
        monkeypatch.setattr("scripts.generate_autodoc_pages.SRC_DIR", src_dir)
        monkeypatch.setattr("scripts.generate_autodoc_pages.OUT_DIR", out_dir)

        src_file = src_dir / "domain" / "my_module.py"
        src_file.parent.mkdir()
        src_file.write_text('"""My docstring."""\n')

        result = generate_markdown(src_file)

        expected_md = out_dir / "domain" / "my_module.md"
        assert result == expected_md
        assert expected_md.exists()
        content = expected_md.read_text()
        assert "# My Module" in content
        assert "::: forging_blocks.domain.my_module" in content

    def test_when_source_without_docstring_then_creates_markdown_without_doc(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        src_dir = tmp_path / "src" / "forging_blocks"
        out_dir = tmp_path / "docs" / "reference" / "autodoc"
        src_dir.mkdir(parents=True)
        out_dir.mkdir(parents=True)
        monkeypatch.setattr("scripts.generate_autodoc_pages.SRC_DIR", src_dir)
        monkeypatch.setattr("scripts.generate_autodoc_pages.OUT_DIR", out_dir)

        src_file = src_dir / "result.py"
        src_file.write_text("x = 1\n")

        result = generate_markdown(src_file)

        expected_md = out_dir / "result.md"
        assert result == expected_md
        content = expected_md.read_text()
        assert "# Result" in content
        assert "x = 1" not in content
        assert "::: forging_blocks.result" in content


@pytest.mark.unit
class TestBuildAutodocSection:
    def test_when_single_file_then_builds_section(self) -> None:
        files = [OUT_DIR / "foundation" / "result.md"]

        section = build_autodoc_section(files)

        assert "- API Reference:" in section
        assert "Foundation:" in section
        assert "Result:" in section

    def test_when_nested_file_then_creates_sublayer(self) -> None:
        files = [OUT_DIR / "application" / "ports" / "inbound" / "use_case.md"]

        section = build_autodoc_section(files)

        assert "Application:" in section
        assert "Ports / Inbound:" in section
        assert "Use Case:" in section

    def test_when_multiple_files_then_groups_by_layer(self) -> None:
        files = [
            OUT_DIR / "domain" / "entity.md",
            OUT_DIR / "application" / "service.md",
            OUT_DIR / "domain" / "value_object.md",
        ]

        section = build_autodoc_section(files)

        assert section.index("Application:") < section.index("Domain:")
        assert "Entity:" in section
        assert "Value Object:" in section
        assert "Service:" in section

    def test_when_empty_list_then_returns_minimal(self) -> None:
        section = build_autodoc_section([])

        assert section == "      - API Reference:"

    def test_when_file_relative_to_has_no_parts_then_skips(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        file = OUT_DIR / "test.md"
        original = Path.relative_to

        def mock_relative_to(self: Path, other: Path) -> Path:
            if self == file and other == OUT_DIR:
                return Path()
            return original(self, other)

        monkeypatch.setattr(Path, "relative_to", mock_relative_to)

        section = build_autodoc_section([file])

        assert section == "      - API Reference:"


@pytest.mark.unit
class TestUpdateNav:
    def test_when_existing_api_reference_then_replaces_it(self) -> None:
        mkdocs = """\
  - Guide: reference/guide.md
  - API Reference:
    - Result: reference/autodoc/foundation/result.md
  - Contributing: contributing.md"""
        section = "  - API Reference:\n    - Result: reference/autodoc/foundation/result.md"

        result = update_nav(mkdocs, section)

        assert result.index("Guide") < result.index("API Reference")
        assert result.index("API Reference") < result.index("Contributing")

    def test_when_no_api_reference_but_has_reference_then_inserts_after(
        self,
    ) -> None:
        mkdocs = """\
  - Guide: reference/guide.md
  - Reference:
      - Some Page: reference/some_page.md
  - Contributing: contributing.md"""
        section = "  - API Reference:\n    - Result: reference/autodoc/result.md"

        result = update_nav(mkdocs, section)

        assert result.index("API Reference") > result.index("Reference:")

    def test_when_neither_section_then_appends_at_end(self) -> None:
        mkdocs = """\
  - Guide: reference/guide.md"""
        section = "  - API Reference:"

        result = update_nav(mkdocs, section)

        assert result.strip().endswith("API Reference:")


@pytest.mark.unit
class TestEnsureAutodocIndex:
    def test_when_index_does_not_exist_then_creates_it(self, tmp_path: Path) -> None:
        ensure_autodoc_index(tmp_path)

        index_file = tmp_path / "index.md"
        assert index_file.exists()
        assert "# API Reference" in index_file.read_text()

    def test_when_index_exists_then_does_not_modify(self, tmp_path: Path) -> None:
        index_file = tmp_path / "index.md"
        index_file.write_text("existing content")

        ensure_autodoc_index(tmp_path)

        assert index_file.read_text() == "existing content"


@pytest.mark.unit
class TestMain:
    def test_when_src_dir_missing_then_exits(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        missing_src = tmp_path / "missing"
        monkeypatch.setattr("scripts.generate_autodoc_pages.SRC_DIR", missing_src)

        with pytest.raises(SystemExit):
            main()

    def test_when_src_exists_then_generates_pages(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        src_dir = tmp_path / "src" / "forging_blocks"
        out_dir = tmp_path / "docs" / "reference" / "autodoc"
        mkdocs_yml = tmp_path / "mkdocs.yml"
        src_dir.mkdir(parents=True)
        out_dir.mkdir(parents=True)
        mkdocs_yml.write_text("nav:\n  - Reference:\n")
        (src_dir / "domain" / "my_module.py").parent.mkdir(parents=True)
        (src_dir / "domain" / "my_module.py").write_text('"""My module."""\n')
        (src_dir / "result.py").write_text("x = 1\n")
        monkeypatch.setattr("scripts.generate_autodoc_pages.SRC_DIR", src_dir)
        monkeypatch.setattr("scripts.generate_autodoc_pages.OUT_DIR", out_dir)
        monkeypatch.setattr("scripts.generate_autodoc_pages.MKDOCS_YML", mkdocs_yml)

        main()

        assert (out_dir / "domain" / "my_module.md").exists()
        assert (out_dir / "result.md").exists()
        assert (out_dir / "index.md").exists()
        updated = mkdocs_yml.read_text()
        assert "API Reference" in updated


@pytest.mark.unit
class TestMainBlock:
    def test_when_run_as_main_then_executes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        script = (
            Path(__file__).resolve().parent.parent.parent
            / "scripts"
            / "generate_autodoc_pages.py"
        )
        src_dir = tmp_path / "src" / "forging_blocks"
        out_dir = tmp_path / "docs" / "reference" / "autodoc"
        mkdocs_yml = tmp_path / "mkdocs.yml"
        src_dir.mkdir(parents=True)
        (src_dir / "module.py").write_text('"""Test."""\n')
        out_dir.mkdir(parents=True)
        mkdocs_yml.write_text("nav:\n  - Reference:\n")
        monkeypatch.chdir(tmp_path)

        code = script.read_text(encoding="utf-8")
        exec(compile(code, str(script), "exec"), {"__name__": "__main__"})

        assert (out_dir / "module.md").exists()
        assert (out_dir / "index.md").exists()
