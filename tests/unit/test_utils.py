"""Unit tests for fin_infra.utils scaffold utilities."""

from pathlib import Path
from string import Template
from unittest.mock import MagicMock, Mock, patch

import pytest

from fin_infra.utils import ensure_init_py, render_template, write


# Note: render_template uses importlib.resources which needs to be mocked at fin_infra.utils.scaffold.pkg


class TestRenderTemplate:
    """Tests for render_template() function."""

    @patch("fin_infra.utils.scaffold.pkg.files")
    def test_render_template_basic(self, mock_files):
        """Test basic template rendering with variable substitution."""
        # Setup mock
        mock_template = Mock()
        mock_template.read_text.return_value = "Hello ${name}!"
        mock_files.return_value.joinpath.return_value = mock_template

        # Execute
        result = render_template("fin_infra.test", "template.tmpl", {"name": "World"})

        # Assert
        assert result == "Hello World!"
        mock_files.assert_called_once_with("fin_infra.test")
        mock_files.return_value.joinpath.assert_called_once_with("template.tmpl")
        mock_template.read_text.assert_called_once_with(encoding="utf-8")

    @patch("fin_infra.utils.scaffold.pkg.files")
    def test_render_template_multiple_variables(self, mock_files):
        """Test template with multiple variables."""
        mock_template = Mock()
        mock_template.read_text.return_value = "class ${Entity}(${Base}):\n    __tablename__ = '${table_name}'"
        mock_files.return_value.joinpath.return_value = mock_template

        result = render_template(
            "fin_infra.budgets.templates",
            "models.py.tmpl",
            {"Entity": "Budget", "Base": "ModelBase", "table_name": "budgets"},
        )

        assert result == "class Budget(ModelBase):\n    __tablename__ = 'budgets'"

    @patch("fin_infra.utils.scaffold.pkg.files")
    def test_render_template_missing_variable_safe_substitute(self, mock_files):
        """Test that missing variables are left as-is (safe_substitute behavior)."""
        mock_template = Mock()
        mock_template.read_text.return_value = "Hello ${name}, your ${role} is ${title}"
        mock_files.return_value.joinpath.return_value = mock_template

        # Only provide 'name', leave 'role' and 'title' missing
        result = render_template("fin_infra.test", "template.tmpl", {"name": "Alice"})

        # safe_substitute leaves missing variables unchanged
        assert result == "Hello Alice, your ${role} is ${title}"

    @patch("fin_infra.utils.scaffold.pkg.files")
    def test_render_template_empty_subs(self, mock_files):
        """Test template rendering with no substitutions."""
        mock_template = Mock()
        mock_template.read_text.return_value = "Static content with no variables"
        mock_files.return_value.joinpath.return_value = mock_template

        result = render_template("fin_infra.test", "template.tmpl", {})

        assert result == "Static content with no variables"

    @patch("fin_infra.utils.scaffold.pkg.files")
    def test_render_template_none_subs(self, mock_files):
        """Test template rendering with None subs (should default to {})."""
        mock_template = Mock()
        mock_template.read_text.return_value = "Content: ${var}"
        mock_files.return_value.joinpath.return_value = mock_template

        result = render_template("fin_infra.test", "template.tmpl", None)

        # None should be converted to {}, so variable remains
        assert result == "Content: ${var}"

    @patch("fin_infra.utils.scaffold.pkg.files")
    def test_render_template_conditional_field(self, mock_files):
        """Test template with conditional field (common pattern)."""
        mock_template = Mock()
        mock_template.read_text.return_value = "class Budget:\n${tenant_field}\n    pass"
        mock_files.return_value.joinpath.return_value = mock_template

        # With tenant field
        result = render_template(
            "fin_infra.test",
            "template.tmpl",
            {"tenant_field": "    tenant_id: str"},
        )
        assert "tenant_id: str" in result

        # Without tenant field (empty string)
        result = render_template("fin_infra.test", "template.tmpl", {"tenant_field": ""})
        assert "tenant_id" not in result
        assert result == "class Budget:\n\n    pass"


class TestWrite:
    """Tests for write() function."""

    def test_write_new_file(self, tmp_path):
        """Test writing a new file."""
        dest = tmp_path / "test.py"
        content = "# Test file\nprint('hello')"

        result = write(dest, content, overwrite=False)

        assert result["action"] == "wrote"
        assert Path(result["path"]).exists()
        assert dest.read_text() == content

    def test_write_creates_parent_directories(self, tmp_path):
        """Test that parent directories are created automatically."""
        dest = tmp_path / "nested" / "deep" / "path" / "file.py"
        content = "# Deep file"

        result = write(dest, content, overwrite=False)

        assert result["action"] == "wrote"
        assert dest.exists()
        assert dest.read_text() == content
        assert dest.parent.exists()

    def test_write_existing_file_no_overwrite(self, tmp_path):
        """Test that existing files are skipped when overwrite=False."""
        dest = tmp_path / "existing.py"
        dest.write_text("Original content")

        result = write(dest, "New content", overwrite=False)

        assert result["action"] == "skipped"
        assert result["reason"] == "exists"
        assert dest.read_text() == "Original content"  # Unchanged

    def test_write_existing_file_with_overwrite(self, tmp_path):
        """Test that existing files are replaced when overwrite=True."""
        dest = tmp_path / "existing.py"
        dest.write_text("Original content")

        result = write(dest, "New content", overwrite=True)

        assert result["action"] == "wrote"
        assert dest.read_text() == "New content"  # Changed

    def test_write_resolves_path(self, tmp_path):
        """Test that paths are resolved to absolute paths."""
        # Create a file in tmp_path
        (tmp_path / "subdir").mkdir()
        dest = tmp_path / "subdir" / "file.py"

        # Write using relative path (Path will resolve it)
        result = write(dest, "content", overwrite=False)

        # Result should contain absolute path
        assert Path(result["path"]).is_absolute()
        assert result["action"] == "wrote"

    def test_write_empty_content(self, tmp_path):
        """Test writing empty content (edge case)."""
        dest = tmp_path / "empty.py"

        result = write(dest, "", overwrite=False)

        assert result["action"] == "wrote"
        assert dest.exists()
        assert dest.read_text() == ""

    def test_write_unicode_content(self, tmp_path):
        """Test writing content with unicode characters."""
        dest = tmp_path / "unicode.py"
        content = "# 你好 世界\n# Здравствуй мир\n# مرحبا بالعالم"

        result = write(dest, content, overwrite=False)

        assert result["action"] == "wrote"
        assert dest.read_text(encoding="utf-8") == content


class TestEnsureInitPy:
    """Tests for ensure_init_py() function."""

    def test_ensure_init_py_creates_file(self, tmp_path):
        """Test creating __init__.py file."""
        content = "# Package marker"

        result = ensure_init_py(tmp_path, overwrite=False, paired=False, content=content)

        assert result["action"] == "wrote"
        init_file = tmp_path / "__init__.py"
        assert init_file.exists()
        assert init_file.read_text() == content

    def test_ensure_init_py_paired_with_reexports(self, tmp_path):
        """Test creating __init__.py with re-exports (paired mode)."""
        content = """from .budget import BudgetModel
from .budget_schemas import Budget, BudgetCreate

__all__ = ["BudgetModel", "Budget", "BudgetCreate"]
"""
        result = ensure_init_py(tmp_path, overwrite=False, paired=True, content=content)

        assert result["action"] == "wrote"
        init_file = tmp_path / "__init__.py"
        assert init_file.exists()
        assert "from .budget import BudgetModel" in init_file.read_text()
        assert "__all__" in init_file.read_text()

    def test_ensure_init_py_skips_existing(self, tmp_path):
        """Test that existing __init__.py is skipped when overwrite=False."""
        init_file = tmp_path / "__init__.py"
        init_file.write_text("# Original")

        result = ensure_init_py(
            tmp_path, overwrite=False, paired=False, content="# New"
        )

        assert result["action"] == "skipped"
        assert result["reason"] == "exists"
        assert init_file.read_text() == "# Original"

    def test_ensure_init_py_overwrites_existing(self, tmp_path):
        """Test that existing __init__.py is replaced when overwrite=True."""
        init_file = tmp_path / "__init__.py"
        init_file.write_text("# Original")

        result = ensure_init_py(tmp_path, overwrite=True, paired=False, content="# New")

        assert result["action"] == "wrote"
        assert init_file.read_text() == "# New"

    def test_ensure_init_py_empty_content(self, tmp_path):
        """Test creating empty __init__.py (minimal package marker)."""
        result = ensure_init_py(tmp_path, overwrite=False, paired=False, content="")

        assert result["action"] == "wrote"
        init_file = tmp_path / "__init__.py"
        assert init_file.exists()
        assert init_file.read_text() == ""

    def test_ensure_init_py_creates_parent_dirs(self, tmp_path):
        """Test that parent directories are created if needed."""
        nested_dir = tmp_path / "nested" / "path"

        result = ensure_init_py(
            nested_dir, overwrite=False, paired=False, content="# Nested"
        )

        assert result["action"] == "wrote"
        assert (nested_dir / "__init__.py").exists()


class TestIntegrationScenarios:
    """Integration tests combining multiple functions."""

    @patch("fin_infra.utils.scaffold.pkg.files")
    def test_render_and_write_workflow(self, mock_files, tmp_path):
        """Test typical workflow: render template then write to file."""
        # Setup mock template
        mock_template = Mock()
        mock_template.read_text.return_value = "class ${Entity}:\n    pass"
        mock_files.return_value.joinpath.return_value = mock_template

        # Render template
        content = render_template(
            "fin_infra.test", "model.tmpl", {"Entity": "Budget"}
        )

        # Write to file
        dest = tmp_path / "budget.py"
        result = write(dest, content, overwrite=False)

        # Verify
        assert result["action"] == "wrote"
        assert dest.read_text() == "class Budget:\n    pass"

    @patch("fin_infra.utils.scaffold.pkg.files")
    def test_full_scaffold_simulation(self, mock_files, tmp_path):
        """Simulate full scaffold workflow: render multiple templates, write files, create __init__.py."""
        # Setup mocks for two templates
        mock_models_tmpl = Mock()
        mock_models_tmpl.read_text.return_value = "class ${Entity}Model: pass"
        mock_schemas_tmpl = Mock()
        mock_schemas_tmpl.read_text.return_value = "class ${Entity}Schema: pass"

        def mock_joinpath(name):
            if name == "models.tmpl":
                return mock_models_tmpl
            elif name == "schemas.tmpl":
                return mock_schemas_tmpl
            return Mock()

        mock_files.return_value.joinpath.side_effect = mock_joinpath

        # Render templates
        models_content = render_template(
            "fin_infra.test", "models.tmpl", {"Entity": "Budget"}
        )
        schemas_content = render_template(
            "fin_infra.test", "schemas.tmpl", {"Entity": "Budget"}
        )

        # Write files
        write(tmp_path / "budget_models.py", models_content, overwrite=False)
        write(tmp_path / "budget_schemas.py", schemas_content, overwrite=False)

        # Create __init__.py
        init_content = """from .budget_models import BudgetModel
from .budget_schemas import BudgetSchema

__all__ = ["BudgetModel", "BudgetSchema"]
"""
        ensure_init_py(tmp_path, overwrite=False, paired=True, content=init_content)

        # Verify all files exist
        assert (tmp_path / "budget_models.py").exists()
        assert (tmp_path / "budget_schemas.py").exists()
        assert (tmp_path / "__init__.py").exists()
        assert "BudgetModel" in (tmp_path / "__init__.py").read_text()
