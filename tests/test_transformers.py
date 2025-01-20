"""
Test cases for transformers.
"""

from typing import Type, Union

from unittest import TestCase

from asplain.transformers.transformer_pipeline import (
    TransformerPipeline,
    ModelSupportPipeline,
    AbductionPipeline,
)


class ReifierTestCase(TestCase):
    """
    Base class for reifier test cases.
    """

    # Style of the fail reports
    maxDiff = None

    # Mandatory attributes (Must be set in the child class)
    TEST_DIR: str = ""
    TEST_PIPELINE_CLASS: Union[Type[TransformerPipeline], None] = None

    # Defaults
    TEST_PROGRAM_FILENAME: str = "prog.lp"
    TEST_EXPECTED_FILENAME: str = "expected.lp"

    def _test_case(self, test_case: str) -> None:
        """
        Loads the files for the given test case and asserts the results of pipeline.
        """
        if self.TEST_PIPELINE_CLASS is None:
            raise ValueError("TEST_PIPELINE_CLASS must be set in the child class")
        else:
            pipeline = self.TEST_PIPELINE_CLASS()  # Instantiate pipeline class

        if self.TEST_DIR is None:
            raise ValueError("TEST_DIR must be set in the child class")

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
    TEST_PIPELINE_CLASS = ModelSupportPipeline

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

    def test_annonymous_variable(self) -> None:
        """
        Test that annonymous variables are correctly renamed.
        [tests/support_reification_tests/test_annonymous_variable]
        """
        self._test_case("test_annonymous_variable")


class AbductionReifier(ReifierTestCase):
    """
    Test cases for abduction reifier.
    """

    TEST_DIR = "./tests/abduction_reification_tests"
    TEST_PIPELINE_CLASS = AbductionPipeline

    def test_fact(self) -> None:
        """
        Tests the correct reification of facts. [tests/abduction_reification_tests/test_fact]

        """
        self._test_case("test_fact")

    def test_rule(self) -> None:
        """
        Tests the correct reification of rules. [tests/abduction_reification_tests/test_rule]

        """
        self._test_case("test_rule")

    def test_pool(self) -> None:
        """
        Tests the correct reification of pools. [tests/abduction_reification_tests/test_pool]

        """
        self._test_case("test_pool")

    def test_aggregates(self) -> None:
        """
        Test that aggregates elements are correctly reified. [tests/support_reification_tests/test_aggregates]

        """
        self._test_case("test_aggregates")

    def test_aggregates_2(self) -> None:
        """
        Test that aggregates elements are correctly reified when within a comparison. [tests/support_reification_tests/test_aggregates_2]

        """
        self._test_case("test_aggregates_2")

    def test_choice_rule(self) -> None:
        """
        Tests that the head aggregate elements are correcly reified. [tests/abduction_reification_tests/test_choice_rule]

        """
        self._test_case("test_choice_rule")

    def test_constraints(self) -> None:
        """
        Test that constraints are correctly reified. [tests/abduction_reification_tests/test_constraints]

        """
        self._test_case("test_constraints")

    def test_annonymous_variable(self) -> None:
        """
        Test that annonymous variables are correctly renamed.
        [tests/abduction_reification_tests/test_annonymous_variable]
        """
        self._test_case("test_annonymous_variable")
