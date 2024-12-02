"""
Test cases for transformers.
"""

from unittest import TestCase

from asplain.transformers.transformer_pipeline import ModelSupportPipeline


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
        self.maxDiff = None  # For a complete output when the test cases fail

        pipeline = ModelSupportPipeline()

        with open(f"{self.TEST_DIR}/{test_case}/expected.lp", "r", encoding="utf-8") as f:
            expected = f.read()

        test_prog_filepath = f"{self.TEST_DIR}/{test_case}/prog.lp"
        result = pipeline.parse_files([test_prog_filepath])

        self.assertEqual(result, expected)

    def test_fact(self) -> None:
        """
        Tests the correct reification of facts. [tests/transformer_tests/test_fact]
        """
        self._test_case("test_fact")

    def test_rule(self) -> None:
        """
        Tests the correct reification of rules. [tests/transformer_tests/test_rule]
        """
        self._test_case("test_rule")

    def test_prevents(self) -> None:
        """
        Tests the correct reification of prevents. [tests/transformer_tests/test_prevents]
        """
        self._test_case("test_prevents")

    def test_choice_rule(self) -> None:
        """
        Tests the correct reification of choice rules. [tests/transformer_tests/test_choice_rule]
        """
        self._test_case("test_choice_rule")

    def test_ignore_constraints(self) -> None:
        """
        Test that constraints are ignored. [tests/transformer_tests/test_ignore_constraints]
        """
        self._test_case("test_ignore_constraints")

    def test_ignore_constraints2(self) -> None:
        """
        Test that constraints are ignored.
        [tests/transformer_tests/test_ignore_constraints2]
        """
        self._test_case("test_ignore_constraints2")

    def test_aggregates(self) -> None:
        """
        Test that aggregates generate the corresponding dependency rules.
        [tests/transformer_tests/test_aggregates]
        """
        self._test_case("test_aggregates")

    # def test_conditional_literals(self) -> None:
    #     """
    #     Test that conditional literals generate the corresponding dependency rules [tests/transformer_tests/test_aggregates]
    #     """
    #     self._test_case("test_aggregates")
