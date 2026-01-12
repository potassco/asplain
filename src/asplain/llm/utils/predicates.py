from enum import Enum
from typing import Tuple

from clorm import ConstantStr, Predicate


class Model(Predicate, name="model"):
    value: ConstantStr


class Label(Predicate, name="label"):
    value: str


class Abducible(Predicate, name="abducible"):
    type: ConstantStr


class RuleFirstOrder(Predicate, name="rule_fo"):
    first_order: str


class Disjunction(Predicate, name="disjunction"):
    id: int


class Normal(Predicate, name="normal"):
    id: int


class Choice(Predicate, name="choice"):
    id: int


class Rule(Predicate, name="rule"):
    head: Disjunction | Normal | Choice
    body: Disjunction | Normal | Choice


class Atom(Predicate, name="atom"):
    atom: ConstantStr


class Tag(Predicate, name="tag"):
    origin: ConstantStr | Model
    node: Rule | Atom
    tag: Label | Abducible | RuleFirstOrder | ConstantStr


class Node(Predicate, name="node"):
    origin: ConstantStr | Model
    id: Rule | Atom


class EdgeSign(ConstantStr, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class Edge(Predicate, name="edge"):
    origin: ConstantStr | Model
    positive: EdgeSign
    edge: Tuple[Rule | Atom, Rule | Atom]
