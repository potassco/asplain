"""Regression tests for LLM environment loading."""

import os
import tempfile
from importlib.util import find_spec
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch


@patch.dict(os.environ, {}, clear=False)
class TestLlmEnv(TestCase):
    """Test loading .env files for optional LLM integrations."""

    def test_load_working_directory_dotenv(self) -> None:
        """Load .env from the current working directory when available."""
        if find_spec("dotenv") is None:
            self.skipTest("python-dotenv is not installed")

        from asplain.llm.utils import load_working_directory_dotenv

        original_cwd = os.getcwd()
        os.environ.pop("OPENAI_API_KEY", None)

        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, ".env").write_text("OPENAI_API_KEY=from-dotenv\n", encoding="utf-8")
            try:
                os.chdir(tmpdir)
                load_working_directory_dotenv()
            finally:
                os.chdir(original_cwd)

        self.assertEqual(os.environ.get("OPENAI_API_KEY"), "from-dotenv")
