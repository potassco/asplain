"""
Test cases for main application functionality.
"""

from unittest import TestCase

from clingo import Control
from clintest.assertion import And, Contains, Not, Or, True_
from clintest.quantifier import All, Exact
from clintest.test import Assert

from asplain.explainers import ContrastiveExplainer

# pylint: disable=R0903


class MockResult:
    """
    Mocking clingo's Result class
    """

    def __init__(self) -> None:
        """
        Create a new mock result.
        """
        self.exhausted = True
        self.interrupted = False
        self.satisfiable = True
        self.unknown = False
        self.unsatisfiable = False


class ExplainerTester:
    """
    Test class for the explainer.
    """

    def __init__(self, explainer, model_symbols, query_include, query_exclude) -> None:
        """
        Create a new tester.

        Args:
            explainer: The explainer to test.
            model_symbols: The symbols of the model to explain.
            query_include: The symbols that must be included in the found model.
            query_exclude: The symbols that must be excluded in the found model.
        """

        self._explainer = explainer
        self._model_symbols = model_symbols
        self._query_include = query_include
        self._query_exclude = query_exclude

    def run_test(self, test) -> None:
        """
        Run a clintest test.

        Args:
            test: The test to run.
        """
        graphs = self._explainer.explain(self._model_symbols, self._query_include, self._query_exclude)
        for graph in graphs:
            ctl = Control(["0"])
            ctl.add("base", [], graph)
            ctl.ground([("base", [])])
            with ctl.solve(yield_=True) as handle:
                for m in handle:
                    test.on_model(m)
        test.on_finish(MockResult())


class TestMain(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_james(self) -> None:
        """
        Test James bond
        """
        ce = ContrastiveExplainer(
            ["./examples/james-bond/encoding.lp"], ["./examples/james-bond/explanation-preference.lp"]
        )
        tester = ExplainerTester(ce, ["d", "p", "h"], [], ["p"])

        # Two models
        test = Assert(Exact(2), True_())
        tester.run_test(test)
        test.assert_()

        # Graphs
        test = Assert(
            All(),
            And(
                Contains("node(d)"),
                Contains("node(p)"),
                Contains("node(h)"),
                Contains("attr(node, p, origin, real)"),
                Contains("attr(node, h, origin, real)"),
                Contains("attr(node, d, origin, real)"),
                Not(Contains("attr(node, a, origin, real)")),
                Not(Contains("attr(node, p, origin, hypothetical)")),
                Or(
                    And(  # Graph abducing d
                        Contains("attr(node, d, abduced, rm)"),
                        Contains("attr(node, h, origin, hypothetical)"),
                        Not(Contains("attr(node, d, origin, hypothetical)")),
                        Not(Contains("attr(node, a, origin, hypothetical)")),
                    ),
                    And(  # Graph abducing h
                        Contains("attr(node, h, abduced, rm)"),
                        Contains("attr(node, d,origin,hypothetical)"),
                        Contains("attr(node, a, origin, hypothetical)"),
                        Not(Contains("attr(node, h, origin, hypothetical)")),
                    ),
                ),
            ),
        )
        tester.run_test(test)
        test.assert_()
