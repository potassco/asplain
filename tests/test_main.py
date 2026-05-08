"""
Test cases for main application functionality.
"""

import tempfile
from importlib.resources import files as files_path
from unittest import TestCase

from clorm.clingo import clingo_main

from asplain import Foil
from asplain.app import AsplainApp
from asplain.utils import logging
from asplain.utils.parser import get_parser


def run_asplain(
    files,
    n_models: int = 0,
    n_explanations: int = 0,
    constants_dict=None,
    q: str = "",
    model: str = "",
    cost_encodings: list[str] = None,
    prunning: list[str] = None,
) -> list[Foil]:
    """
    Run the main application with the given arguments.
    """
    foils = []
    if constants_dict is None:
        constants_dict = {}
    if cost_encodings is None:
        cost_encodings = []
    if prunning is None:
        prunning = []

    def save_foil(foil) -> None:
        foils.append(foil)

    args = files + [
        "--nexplanations",
        str(n_explanations),
        "--query",
        q,
        "-n",
        str(n_models),
    ]
    if model:
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".lp", encoding="utf-8") as f:
            f.write(model)
            args += ["--model", f.name]
    for ce in cost_encodings or []:
        args += ["--cost-encoding", ce]
    for pe in prunning or []:
        args += ["--prune", pe]

    print("------- test running asplain with arguments:", args)
    clingo_main(
        AsplainApp("asplain", constants=constants_dict, on_foil=save_foil),
        arguments=args,
    )
    return foils


def compare_expected(foils, expected):
    assert len(foils) == len(expected), f"Expected {len(expected)} foils, but got {len(foils)}"
    assert set(foils) == set(expected), (
        f"Foils do not match expected.\n"
        f"Got: {[f.__dict__ for f in foils]}\n"
        f"Expected: {[e.__dict__ for e in expected]}"
    )


def check_facts(foil: Foil, expected_facts: list[str], expected_not_facts: list[str]) -> None:
    for fact in expected_facts:
        assert fact in foil.explanation_graph_facts, f"Expected fact '{fact}' not found in explanation graph."
    for fact in expected_not_facts:
        assert fact not in foil.explanation_graph_facts, f"Unexpected fact '{fact}' found in explanation graph."


class TestMain(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_parser(self) -> None:
        """
        Test the parser.
        """
        parser = get_parser()
        ret = parser.parse_args(["--log", "info"])
        self.assertEqual(ret.log, logging.INFO)

    def test_app_james(self) -> None:
        """
        Test the main application with a simple example.
        """
        files = ["examples/james-bond/encoding.lp"]

        model = "c. a."
        foils = run_asplain(files, n_models=0, n_explanations=1, q="p ", model=model)
        expected = [
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"p", "d"},
                added_rules=set(),
                removed_rules={"c.", "a."},
            )
        ]
        compare_expected(foils, expected)
        foils = run_asplain(files, n_models=0, n_explanations=1, q="p ")
        expected = expected + [
            Foil(
                reference_atoms={"d", "c", "a"},
                foil_atoms={"p", "d"},
                added_rules=set(),
                removed_rules={"c.", "a."},
            ),
        ]
        compare_expected(foils, expected)

        foils = run_asplain(files, n_models=0, n_explanations=0, q="p ", model=model)
        expected = [
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"p", "d"},
                added_rules=set(),
                removed_rules={"c.", "a."},
            ),
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"p", "t", "d"},
                added_rules={"t."},
                removed_rules={"c.", "a."},
            ),
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"a", "p", "t"},
                added_rules={"t."},
                removed_rules={"c."},
            ),
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"a", "p", "t", "d"},
                added_rules={"t."},
                removed_rules={"c."},
            ),
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"p", "t"},
                added_rules={"t."},
                removed_rules={"c.", "a."},
            ),
        ]
        compare_expected(foils, expected)

        cost_encoding_pd = files_path("asplain.encodings").joinpath("costs").joinpath("program-difference.lp")
        foils = run_asplain(
            files, n_models=0, n_explanations=0, q="p ", model=model, cost_encodings=[str(cost_encoding_pd)]
        )
        expected = [
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"p", "d"},
                added_rules=set(),
                removed_rules={"c.", "a."},
            ),
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"a", "p", "t"},
                added_rules={"t."},
                removed_rules={"c."},
            ),
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"a", "p", "t", "d"},
                added_rules={"t."},
                removed_rules={"c."},
            ),
        ]
        compare_expected(foils, expected)

        cost_encoding_pd = files_path("asplain.encodings").joinpath("costs").joinpath("program-difference.lp")
        cost_encoding_md = files_path("asplain.encodings").joinpath("costs").joinpath("model-difference.lp")
        foils = run_asplain(
            files,
            n_models=0,
            n_explanations=0,
            q="p ",
            model=model,
            cost_encodings=[str(cost_encoding_pd), str(cost_encoding_md)],
        )
        expected = [
            Foil(
                reference_atoms={"c", "a"},
                foil_atoms={"a", "p", "t"},
                added_rules={"t."},
                removed_rules={"c."},
            ),
        ]
        compare_expected(foils, expected)
        expected_facts = [
            "node(d,atom).",
            "node(a,atom).",
            "program(d,ref).",
            "program(a,ref).",
            "model(a,ref).",
            "model(a,foil).",
        ]
        check_facts(foils[0], expected_facts, [])

        foils = run_asplain(
            files,
            n_models=0,
            n_explanations=0,
            q="p ",
            model=model,
            cost_encodings=[str(cost_encoding_pd), str(cost_encoding_md)],
            prunning=["CHANGES"],
        )
        expected_facts = [
            "node(t,atom).",
            "node(p,atom).",
            "node(c,atom).",
            "program(t,foil).",
            "model(t,foil).",
            "model(c,ref).",
        ]
        expected_facts_not = [
            "node(d,atom).",
            "node(a,atom).",
            "program(d,ref).",
            "program(a,ref).",
            "model(a,ref).",
            "model(a,foil).",
        ]
        check_facts(foils[0], expected_facts, expected_facts_not)
