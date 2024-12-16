"""
Test cases for transformers.
"""

from unittest import TestCase

from asplain.transformers.transformer_pipeline import ModelSupportPipeline


class ReifierTestCase(TestCase):

    maxDiff = None
    TEST_DIR = None  # Must be set in the child class

    # Defaults
    TEST_PROGRAM_FILENAME = "prog.lp"
    TEST_EXPECTED_FILENAME = "expected.lp"

    def _test_case(self, test_case: str) -> None:
        """
        Loads the files for the given test case and asserts the results of pipeline.
        """
        pipeline = ModelSupportPipeline()

        with open(f"{self.TEST_DIR}/{test_case}/{self.TEST_EXPECTED_FILENAME}", "r", encoding="utf-8") as f:
            expected = f.read()

        test_prog_filepath = f"{self.TEST_DIR}/{test_case}/{self.TEST_PROGRAM_FILENAME}"
        result = pipeline.parse_files([test_prog_filepath])
        result_lines = result.splitlines()
        expected_lines = expected.splitlines()
        self.assertEqual(result_lines, expected_lines)


class TestExplainabilityReifier(ReifierTestCase):
    """
    Test cases for explainability reifier.
    """

    TEST_DIR = "./tests/support_reification_tests"

    def test_fact(self) -> None:
        """
        Tests the correct reification of facts. [tests/support_reification_tests/test_fact]

        """
        self._test_case("test_fact")

    def test_rule(self) -> None:
        """
        Tests the correct reification of rules. [tests/support_reification_tests/test_rule]

        """
        self._test_case("test_rule")

    def test_prevents(self) -> None:
        """
        Tests the correct reification of prevents. [tests/support_reification_tests/test_prevents]

        """
        self._test_case("test_prevents")

    def test_choice_rule(self) -> None:
        """
        Tests the correct reification of choice rules. [tests/support_reification_tests/test_choice_rule]

        """
        self._test_case("test_choice_rule")

    def test_constraints(self) -> None:
        """
        Test that constraints are ignored. [tests/support_reification_tests/test_constraints]

        """
        self._test_case("test_constraints")

    def test_aggregates(self) -> None:
        """
        Test that aggregates generate the corresponding dependency rules.
        [tests/support_reification_tests/test_aggregates]

        """
        self._test_case("test_aggregates")
