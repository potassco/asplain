"""
Test cases for main application functionality.
"""

import tempfile
from importlib.resources import files as files_path
from pathlib import Path
from typing import Optional
from unittest import TestCase
from unittest.mock import patch

from clorm.clingo import clingo_main

from asplain import Foil
from asplain.app import AsplainApp
from asplain.utils import logging
from asplain.utils.parser import get_parser


def run_asplain(  # pylint: disable=too-many-positional-arguments
    files: list[str],
    n_models: int = 0,
    n_explanations: int = 0,
    constants_dict: Optional[dict[str, str]] = None,
    q: str = "",
    model: str = "",
    cost_encodings: Optional[list[str]] = None,
    prunning: Optional[list[str]] = None,
    assumptions: str = "",
    dynamic_tags: Optional[list[str]] = None,
) -> list[Foil]:
    """
    Run the main application with the given arguments.

    Args:
        files: List of file paths to load.
        n_models: Number of models to generate.
        n_explanations: Number of explanations to generate.
        constants_dict: Dictionary of constants to pass to clingo.
        q: Query to explain.
        model: Reference model to use for explanations.
        cost_encodings: List of cost encodings to use.
        prunning: List of prunning methods to use.
        assumptions: Assumptions to include as integrity constraints as a single string
        dynamic_tags: List of encodings to use for dynamic tags.
    """
    foils = []
    if constants_dict is None:
        constants_dict = {}
    if cost_encodings is None:
        cost_encodings = []
    if prunning is None:
        prunning = []
    if dynamic_tags is None:
        dynamic_tags = []

    def save_foil(foil: Foil) -> None:
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
    if assumptions:
        args += ["--assumptions", assumptions]
    for dt in dynamic_tags or []:
        args += ["--dynamic-tags", dt]

    print("------- test running asplain with arguments:", args)
    clingo_main(
        AsplainApp("asplain", constants=constants_dict, on_foil=save_foil),
        arguments=args,
    )
    return foils


def compare_expected(foils: list[Foil], expected: list[Foil]) -> None:
    """
    Compare the obtained foils with the expected ones.
    Assert that the number of foils is the same, and that each foil matches the expected one
    regardless of the order.

    Args:
        - foils: List of obtained foils.
        - expected: List of expected foils.
    """

    assert len(foils) == len(expected), f"Expected {len(expected)} foils, but got {len(foils)}"
    assert set(foils) == set(expected), f"Foils do not match expected.\n" f"Got:      {foils}\n" f"Expected: {expected}"


def check_facts(foil: Foil, expected: list[str], not_expected: list[str]) -> None:
    """
    Check that the expected facts are present in the foil's explanation graph facts,
    and that the expected not facts are not present.
    Args:
        - foil: The foil whose explanation graph facts to check.
        - expected: List of facts that should be present in the explanation graph.
        - not_expected: List of facts that should not be present in the explanation graph.
    """
    for fact in expected:
        assert fact in foil.explanation_graph_facts, f"Expected fact '{fact}' not found in explanation graph."
    for fact in not_expected:
        assert fact not in foil.explanation_graph_facts, f"Unexpected fact '{fact}' found in explanation graph."


# --- File constants ---

JAMES_FILE = str(Path("examples").joinpath("james-bond").joinpath("encoding.lp"))

# Cost encodings
COST_ASSUMPTIONS = str(
    files_path("asplain.encodings").joinpath("costs").joinpath("penalize-non-assumptions-removed.lp")
)
COST_ADDED = str(files_path("asplain.encodings").joinpath("costs").joinpath("penalize-added.lp"))
COST_PD = str(files_path("asplain.encodings").joinpath("costs").joinpath("program-difference.lp"))
COST_MD = str(files_path("asplain.encodings").joinpath("costs").joinpath("model-difference.lp"))

# Dynamic tag encodings
DYNAMIC_TAGS_ASSUMPTIONS = str(
    files_path("asplain.encodings").joinpath("dynamic-tags").joinpath("removable-assumptions.lp")
)


class TestMain(TestCase):
    """Test cases for main application functionality."""

    def setUp(self) -> None:
        self.files = [JAMES_FILE]
        self.mock_graphviz = patch("asplain.utils.viz.render").start()
        self.addCleanup(patch.stopall)

    def test_parser(self) -> None:
        """Test the parser."""
        parser = get_parser()
        ret = parser.parse_args(["--log", "info"])
        self.assertEqual(ret.log, logging.INFO)

    def test_app_james_basic(self) -> None:
        """Test basic foil generation without assumptions."""
        foils = run_asplain(self.files, n_models=0, n_explanations=1, q="p ", model="c. a.")
        compare_expected(
            foils,
            [
                Foil(reference_atoms=["c", "a"], foil_atoms=["p", "d"], added_rules=[], removed_rules=["c.", "a."]),
            ],
        )

        foils = run_asplain(self.files, n_models=0, n_explanations=1, q="p ")
        compare_expected(
            foils,
            [
                Foil(reference_atoms=["c", "a"], foil_atoms=["p", "d"], added_rules=[], removed_rules=["c.", "a."]),
                Foil(
                    reference_atoms=["d", "c", "a"], foil_atoms=["p", "d"], added_rules=[], removed_rules=["c.", "a."]
                ),
            ],
        )

    def test_app_james_assumptions(self) -> None:
        """Test foil generation with assumptions."""
        foils = run_asplain(self.files, n_models=0, n_explanations=0, q="p ", assumptions="-d")
        compare_expected(
            foils,
            [
                Foil(reference_atoms=["c", "a"], foil_atoms=["p", "a", "t"], added_rules=["t."], removed_rules=["c."]),
                Foil(reference_atoms=["c", "a"], foil_atoms=["p", "t"], added_rules=["t."], removed_rules=["c.", "a."]),
            ],
        )

        foils = run_asplain(
            self.files,
            n_models=0,
            n_explanations=0,
            q="p ",
            assumptions="-d",
            cost_encodings=[COST_ASSUMPTIONS, COST_ADDED],
            dynamic_tags=[DYNAMIC_TAGS_ASSUMPTIONS],
        )
        compare_expected(
            foils,
            [
                Foil(
                    reference_atoms=["c", "a"],
                    foil_atoms=["p", "d"],
                    added_rules=[],
                    removed_rules=["c.", "a.", "#false :- d."],
                ),
            ],
        )

    def test_app_james_unsat(self) -> None:
        """Test foil generation in UNSAT cases."""
        foils = run_asplain(
            self.files,
            n_models=0,
            n_explanations=0,
            q="",
            assumptions="-c -d",
            cost_encodings=[COST_ASSUMPTIONS, COST_PD],
            dynamic_tags=[DYNAMIC_TAGS_ASSUMPTIONS],
        )
        compare_expected(
            foils,
            [
                Foil(reference_atoms=[], foil_atoms=["a", "c"], added_rules=[], removed_rules=["#false :- c."]),
            ],
        )

    def test_app_james_cost_encodings(self) -> None:
        """Test foil generation with various cost encoding combinations."""
        model = "c. a."

        # No cost encoding
        foils = run_asplain(self.files, n_models=0, n_explanations=0, q="p ", model=model)
        compare_expected(
            foils,
            [
                Foil(reference_atoms=["c", "a"], foil_atoms=["p", "d"], added_rules=[], removed_rules=["c.", "a."]),
                Foil(
                    reference_atoms=["c", "a"],
                    foil_atoms=["p", "t", "d"],
                    added_rules=["t."],
                    removed_rules=["c.", "a."],
                ),
                Foil(reference_atoms=["c", "a"], foil_atoms=["a", "p", "t"], added_rules=["t."], removed_rules=["c."]),
                Foil(
                    reference_atoms=["c", "a"],
                    foil_atoms=["a", "p", "t", "d"],
                    added_rules=["t."],
                    removed_rules=["c."],
                ),
                Foil(reference_atoms=["c", "a"], foil_atoms=["p", "t"], added_rules=["t."], removed_rules=["c.", "a."]),
            ],
        )

        # Program difference cost
        foils = run_asplain(self.files, n_models=0, n_explanations=0, q="p ", model=model, cost_encodings=[COST_PD])
        compare_expected(
            foils,
            [
                Foil(reference_atoms=["c", "a"], foil_atoms=["p", "d"], added_rules=[], removed_rules=["c.", "a."]),
                Foil(reference_atoms=["c", "a"], foil_atoms=["a", "p", "t"], added_rules=["t."], removed_rules=["c."]),
                Foil(
                    reference_atoms=["c", "a"],
                    foil_atoms=["a", "p", "t", "d"],
                    added_rules=["t."],
                    removed_rules=["c."],
                ),
            ],
        )

        # Program + model difference cost
        foils = run_asplain(
            self.files, n_models=0, n_explanations=0, q="p ", model=model, cost_encodings=[COST_PD, COST_MD]
        )
        compare_expected(
            foils,
            [
                Foil(reference_atoms=["c", "a"], foil_atoms=["a", "p", "t"], added_rules=["t."], removed_rules=["c."]),
            ],
        )
        expected = [
            "node(d,atom).",
            "node(a,atom).",
            "program(d,ref).",
            "program(a,ref).",
            "model(a,ref).",
            "model(a,foil).",
        ]
        check_facts(foils[0], expected, [])

    def test_app_james_pruning(self) -> None:
        """Test foil generation with pruning enabled."""
        model = "c. a."
        foils = run_asplain(
            self.files,
            n_models=0,
            n_explanations=0,
            q="p ",
            model=model,
            cost_encodings=[COST_PD, COST_MD],
            prunning=["CHANGES"],
        )
        check_facts(
            foils[0],
            expected=[
                "node(t,atom).",
                "node(p,atom).",
                "node(c,atom).",
                "program(t,foil).",
                "model(t,foil).",
                "model(c,ref).",
            ],
            not_expected=[
                "node(d,atom).",
                "node(a,atom).",
                "program(d,ref).",
                "program(a,ref).",
                "model(a,ref).",
                "model(a,foil).",
            ],
        )
