"""
Test cases for transformers.
"""

from io import StringIO
from typing import Union
from unittest import TestCase

from asplain.utils import logging
from asplain.utils.logging import configure_logging, get_logger
from asplain.utils.parser import get_parser

from asplain.transformers.transformer_pipeline import TransformerPipeline, ModelSupportPipeline


class TestMain(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_logger(self) -> None:
        """
        Test the logger.
        """
        sio = StringIO()
        configure_logging(sio, logging.INFO, True)
        log = get_logger("main")
        log.info("test123")
        self.assertRegex(sio.getvalue(), "test123")

    def test_parser(self) -> None:
        """
        Test the parser.
        """
        parser = get_parser()
        ret = parser.parse_args(["--log", "info"])
        self.assertEqual(ret.log, logging.INFO)


class TestExplainabilityReifier(TestCase):
    """
    Test cases for explainability reifier.
    """

    TEST_DIR = "/home/velka/projs/asp/asplain/tests/transformer_tests"

    def _test_case(self, test_case: str) -> None:
        """
        Loads the files for the given test case and asserts the results of pipeline.
        """
        # Config test
        self.maxDiff = None

        pipeline = ModelSupportPipeline()

        with open(f"{self.TEST_DIR}/{test_case}/expected.lp", "r", encoding="utf-8") as f:
            expected = f.read()

        test_prog_filepath = f"{self.TEST_DIR}/{test_case}/prog.lp"
        result = pipeline.parse_files([test_prog_filepath])

        self.assertEqual(result, expected)

    def test_fact(self):
        """
        Tests the correct reification of facts. [tests/transformer_tests/test_fact]
        """
        self._test_case("test_fact")

    def test_rule(self):
        """
        Tests the correct reification of rules. [tests/transformer_tests/test_rule]
        """
        self._test_case("test_rule")

    def test_prevents(self):
        """
        Tests the correct reification of prevents. [tests/transformer_tests/test_prevents]
        """
        self._test_case("test_prevents")

    def test_choice_rule(self):
        """
        Tests the correct reification of choice rules. [tests/transformer_tests/test_choice_rule]
        """
        self._test_case("test_choice_rule")

    def test_ignore_constraints(self):
        """
        Test that constraints are ignored.
        """
        self._test_case("test_ignore_constraints")
