import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple, Set

from clorm import Predicate, ConstantStr, FactBase
from clorm.clingo import Model as ClormModel
from clorm.clingo import Control


class Origin(ConstantStr, Enum):
    REFERENCE = "reference"
    REFERENCE_MODEL = "model(reference)"
    FOIL = "foil"
    FOIL_MODEL = "model(foil)"


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


class Rule(Predicate, name="rule"):
    head: Disjunction | Normal
    body: Disjunction | Normal


class Atom(Predicate, name="atom"):
    atom: ConstantStr


class Tag(Predicate, name="tag"):
    origin: Origin
    node: Rule | Atom
    tag: Label | Abducible | RuleFirstOrder | ConstantStr


class Node(Predicate, name="node"):
    origin: Origin
    entity: Rule | Atom


class EdgeSign(ConstantStr, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class Edge(Predicate, name="edge"):
    origin: Origin
    positive: EdgeSign
    edge: Tuple[Rule | Atom, Rule | Atom]


@dataclass
class TagBehaviour:
    tag: Abducible
    include: bool

    def __hash__(self) -> int:
        return hash(self.tag)


class Graph:

    def __init__(self, contrastive_program_graph: str) -> None:
        self.contrastive_program_graph = contrastive_program_graph
        self._facts: Optional[FactBase] = None
        self._behaviours = {TagBehaviour(Abducible("remove"), include=False)}

        print(self.contrastive_program_graph)

        self.get_facts(self.contrastive_program_graph)

    def _on_facts_model(self, model: ClormModel) -> None:
        self._facts = model.facts(atoms=True)

    def get_facts(self, program: str) -> None:
        ctl = Control(unifier=[Tag, Node, Edge])
        ctl.add("base", [], program)
        ctl.ground([("base", [])])
        ctl.solve(on_model=self._on_facts_model)

    def json(self) -> str:
        nodes = [
            node_to_json_dict(n, self._facts, behaviours=self._behaviours)
            for n in self._facts.query(Node).select(Node).all()
        ]
        nodes = filter(lambda x: x is not None, nodes)
        edges = [edge_to_json_dict(e) for e in self._facts.query(Edge).select(Edge).all()]

        return json.dumps([nodes, edges])


def tag_to_json_dict(tag: Tag) -> Dict[str, str | int]:
    return {
        "tag": str(tag.tag),
        "origin": tag.origin.value,
    }


def edge_to_json_dict(edge: Edge) -> Dict[str, str | int | bool]:
    return {
        "type": "edge",
        "source": str(edge.edge[0]),
        "target": str(edge.edge[1]),
        "positive": str(edge.positive),
        "label": str(edge.edge),
        "origin": edge.origin.value,
    }


def node_to_json_dict(node: Node, facts: FactBase, behaviours: Set[TagBehaviour]) -> Dict[str, str | int] | None:
    tag_query = facts.query(Tag).where(Tag.node == node.entity).select(Tag)
    tags = [t.tag for t in tag_query.all()]

    for behaviour in behaviours:
        if not behaviour.include and behaviour.tag in tags:
            return None

    json_tags = [tag_to_json_dict(tag) for tag in tag_query.all()]
    return {
        "type": "node",
        "label": str(node.entity),
        "origin": node.origin.value,
        "tags": json_tags,
    }
