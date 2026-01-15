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
    EdgeSign,
    Label,
    Node,
    Normal,
    Rule,
    RuleFirstOrder,
    Tag,
)
from .processes import ProcessAbducibleRemoved, TagProcess

RULE_ID_PREDICATE = "rule"


class Origin(Enum):
    REFERENCE = "reference"
    REFERENCE_MODEL = "model(reference)"
    FOIL = "foil"
    FOIL_MODEL = "model(foil))"


class RuleType(Enum):
    ATOM = "atom"
    NORMAL = "normal"
    DISJUNCTION = "disjunction"
    CHOICE = "choice"


class RuleIDSet:
    def __init__(self) -> None:
        self._data: Dict[str, int] = {}
        self._id: int = 1

    def add(self, item: str) -> int:
        if item not in self._data:
            self._data[item] = self._id
            self._id += 1
        return self._data[item]

    def get(self, item: str) -> Optional[int]:
        return self._data.get(item)

    def get_by_id(self, index: int) -> Optional[str]:
        if index > len(self._data) or index <= 0:
            return None
        (rule_id, _) = sorted(self._data.items(), key=lambda item: item[1])[index]
        return rule_id


@dataclass
class GraphNode:
    id: str
    rule_type: RuleType
    origins: Set[str]
    tags: Dict[str, str | int | bool]


@dataclass
class GraphEdge:
    source: str
    target: str
    origins: Set[str]
    sign: EdgeSign


class Graph:
    def __init__(self, contrastive_program_graph: str) -> None:
        self._rule_ids = RuleIDSet()
        self._graph: str = contrastive_program_graph
        self._facts: Optional[FactBase] = None
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[Tuple[str, str], GraphEdge] = {}
        self._tag_processes: Set[TagProcess] = {
            ProcessAbducibleRemoved(),
        }

        self.get_facts(self._graph)
        self.compute_nodes()
        self.compute_edges()
        self.compute_tags()

    def json(self) -> Dict[str, List[Dict[str, str | int | bool]]]:
        json_nodes = []
        for node in self._nodes.values():
            json_node = {
                "type": node.rule_type.value,
                "id": node.id,
                "origins": list(node.origins),
                **node.tags,
            }
            json_nodes.append(json_node)
        json_edges = []
        for edge in self._edges.values():
            json_edge = {
                "type": edge.sign.value,
                "source": edge.source,
                "target": edge.target,
                "origins": list(edge.origins),
            }
            json_edges.append(json_edge)
        return {"nodes": json_nodes, "edges": json_edges}

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
            return RuleType.ATOM
        match rule.head:
            case Normal():
                return RuleType.NORMAL
            case Disjunction():
                return RuleType.DISJUNCTION
            case Choice():
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

    def parse_rule_id(self, rule: Atom | Rule) -> str:
        match rule:
            case Atom():
                return str(rule)
            case Rule():
                rule_id = self._rule_ids.add(str(rule))
                return f"{RULE_ID_PREDICATE}({rule_id})"

    def compute_nodes(self) -> None:
        if self._facts is None:
            return
        query_nodes = self._facts.query(Node).select(Node)
        for node in query_nodes.all():
            node_string = str(node.id)
            if node_string not in self._nodes:
                # Create & register GraphNode
                rule_type = self.parse_rule_type(node)
                rule_id = self.parse_rule_id(node.id)
                graph_node = GraphNode(
                    id=rule_id,
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
                rule_id_source = self.parse_rule_id(edge_source)
                rule_id_target = self.parse_rule_id(edge_target)
                graph_edge = GraphEdge(
                    source=rule_id_source,
                    target=rule_id_target,
                    origins={str(edge.origin)},
                    sign=edge.positive,
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
