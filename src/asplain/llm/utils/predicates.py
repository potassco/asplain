from enum import Enum

from clorm import ConstantStr, Predicate, Raw
from clorm.orm.types import HeadList


class RuleType(ConstantStr, Enum):
    DISJUNCTION = "disjunction"
    NORMAL = "normal"
    CHOICE = "choice"


class Rule(Predicate, name="rule"):
    type: RuleType


class Node(Predicate, name="node"):
    element: Raw
    type: ConstantStr | Rule


class World(ConstantStr, Enum):
    REFERENCE = "ref"
    FOIL = "foil"


class Model(Predicate, name="model"):
    node: Raw
    world: World


class Program(Predicate, name="program"):
    node: Raw
    world: World


class TagLabel(Predicate, name="label"):
    label: str
    variables: Raw


class TagRuleLocation(Predicate, name="rule_loc"):
    column: int
    file: str
    line: int


class TagRuleFirstOrder(Predicate, name="rule_fo"):
    first_order: str


class Tag(Predicate, name="tag"):
    node: Raw
    tag: ConstantStr | TagLabel | TagRuleLocation | TagRuleFirstOrder


class EdgeNodes(Predicate, is_tuple=True):
    source: Raw
    target: Raw


class Edge(Predicate, name="edge"):
    nodes: EdgeNodes
    positive: int


class Query(Predicate, name="query"):
    node: Raw
    included: int


class Fired(Predicate, name="fired"):
    node: Raw
