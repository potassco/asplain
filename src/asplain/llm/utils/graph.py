from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from warnings import warn

from clorm import FactBase
from clorm.clingo import ClormControl, ClormModel

from .predicates import (
    Abducible,
    Atom,
    Choice,
    Disjunction,
    Edge,
    Label,
    Node,
    Normal,
    RuleFirstOrder,
    Tag,
)
from .processes import ProcessAbducibleRemoved, TagProcess


class Origin(Enum):
    REFERENCE = "reference"
    REFERENCE_MODEL = "model(reference)"
    FOIL = "foil"
    FOIL_MODEL = "model(foil))"


class RuleType(Enum):
    NORMAL = "normal"
    DISJUNCTION = "disjunction"
    CHOICE = "choice"


@dataclass
class GraphNode:
    id: str
    rule_type: RuleType
    origins: Set[str]
    tags: Dict[str, str | int | bool]


@dataclass
class GraphEdge:
    id: str
    source: str
    target: str
    origins: Set[str]


class Graph:
    def __init__(self, contrastive_program_graph: str) -> None:
        self._graph: str = contrastive_program_graph
        self._facts: Optional[FactBase] = None
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[Tuple[str, str], GraphEdge] = {}
        self._tag_processes: Set[TagProcess] = {
            ProcessAbducibleRemoved(),
        }

        print("GRAPH", self._graph)

        self.get_facts(self._graph)

        print("FACTS", self._facts)

        self.compute_nodes()

        print("NODES", self._nodes)

        self.compute_edges()

        print("EDGES", self._edges)

        self.compute_tags()

        print("NODES", self._nodes)

    def json(self) -> Dict[str, List[Dict[str, str | int | bool]]]:
        return {"nodes": [], "edges": []}

    def _on_facts_model(self, model: ClormModel) -> None:
        self._facts = model.facts(atoms=True)

    def get_facts(self, program: str) -> None:
        ctl = ClormControl(unifier=[Tag, Node, Edge])
        ctl.add("base", [], program)
        ctl.ground([("base", [])])
        ctl.solve(on_model=self._on_facts_model)

    def parse_rule_type(self, node: Node) -> RuleType:
        rule = node.id
        if isinstance(rule, Atom):
            return RuleType.NORMAL
        match rule.head:
            case Normal():
                print("T NORMAL", node)
                return RuleType.NORMAL
            case Disjunction():
                print("T DISJUNCTION", node)
                return RuleType.DISJUNCTION
            case Choice():
                print("T CHOICE", node)
                return RuleType.CHOICE

    def parse_tag(self, tag: Tag) -> Tuple[str, str | bool]:
        match tag.tag:
            case str():
                return str(tag.tag), True
            case Label():
                return "label", tag.tag.value
            case Abducible():
                return "abducible", tag.tag.type
            case RuleFirstOrder():
                return "rule_fo", tag.tag.first_order

    def compute_nodes(self) -> None:
        if self._facts is None:
            return
        query_nodes = self._facts.query(Node).select(Node)
        for node in query_nodes.all():
            node_string = str(node.id)
            if node_string not in self._nodes:
                # Create & register GraphNode
                rule_type = self.parse_rule_type(node)
                graph_node = GraphNode(
                    id=node_string,
                    rule_type=rule_type,
                    origins={str(node.origin)},
                    tags={},
                )
                self._nodes[node_string] = graph_node
            else:
                # Add origin to GraphNode
                graph_node = self._nodes.get(node_string)
                if graph_node is None:
                    continue
                graph_node.origins.add(str(node.origin))

    def compute_edges(self) -> None:
        if self._facts is None:
            return
        query_edges = self._facts.query(Edge).select(Edge)
        for edge in query_edges.all():
            (edge_source, edge_target) = edge.edge
            edge_tuple = (str(edge_source), str(edge_target))
            if edge_tuple not in self._edges:
                graph_edge = GraphEdge(
                    id=str(edge_tuple),
                    source=str(edge_source),
                    target=str(edge_target),
                    origins={str(edge.origin)},
                )
                self._edges[edge_tuple] = graph_edge
            else:
                graph_edge = self._edges.get(edge_tuple)
                if graph_edge is None:
                    continue
                graph_edge.origins.add(str(edge.origin))

    def compute_tags(self) -> None:
        if self._facts is None:
            return
        query_tags = self._facts.query(Tag).select(Tag)
        for tag in query_tags.all():
            node_string = str(tag.node)
            graph_node = self._nodes.get(node_string)
            if graph_node is None:
                warn(f"No matching node found for tag: {str(tag)}")
                continue
            tag_id, tag_value = self.parse_tag(tag)
            graph_node.tags[tag_id] = tag_value
