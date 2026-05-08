"""
Clorm Predicates representing the explanation graph
"""

from enum import Enum

from clorm import ConstantStr, Predicate, Raw

# pylint: disable=abstract-method


class RuleType(ConstantStr, Enum):
    """Type of a rule"""

    DISJUNCTION = "disjunction"
    NORMAL = "normal"
    CHOICE = "choice"


class Rule(Predicate, name="rule"):
    """Representation of a program rule"""

    type: RuleType


class Node(Predicate, name="node"):
    """Node in the explanation graph"""

    element: Raw
    type: ConstantStr | Rule


class World(ConstantStr, Enum):
    """Type of model worlds where a node could be situated in"""

    REFERENCE = "ref"
    FOIL = "foil"


class Model(Predicate, name="model"):
    """Association of a model node with a world"""

    node: Raw
    world: World


class Program(Predicate, name="program"):
    """Association of a program node with a world"""

    node: Raw
    world: World


class TagLabel(Predicate, name="label"):
    """Node tag with a label"""

    label: str
    variables: Raw


class TagRuleLocation(Predicate, name="rule_loc"):
    """Node tag with the file location of a rule"""

    column: int
    file: str
    line: int


class TagRuleFirstOrder(Predicate, name="rule_fo"):
    """Node tag with the first order rule"""

    first_order: str


class Tag(Predicate, name="tag"):
    """Tag for a node"""

    node: Raw
    tag: ConstantStr | TagLabel | TagRuleLocation | TagRuleFirstOrder


class EdgeNodes(Predicate, is_tuple=True):
    """Nodes connected by an edge"""

    source: Raw
    target: Raw


class Edge(Predicate, name="edge"):
    """Edge in the explanation graph"""

    nodes: EdgeNodes
    positive: int


class Query(Predicate, name="query"):
    """Query node for the explanation"""

    node: Raw
    included: int


class Fired(Predicate, name="fired"):
    """Node that fired"""

    node: Raw
