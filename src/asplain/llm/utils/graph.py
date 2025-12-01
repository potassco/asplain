import json
import warnings
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Tuple

import clingo


class Origin(Enum):
    REFERENCE = "reference"
    REFERENCE_MODEL = "model(reference)"
    FOIL = "foil"
    FOIL_MODEL = "model(foil)"


@dataclass
class NodeJSON:
    id: int
    label: str
    origin: Origin

    def __str__(self) -> str:
        return f"<Node {self.id}: {self.label}>"

    def json_dict(self) -> Dict[str, str | int]:
        return {
            "type": "node",
            "id": self.id,
            "label": self.label,
            "origin": self.origin.value,
        }

    __repr__ = __str__


@dataclass
class EdgeJSON:
    id: int
    label: Optional[str]
    source_id: int
    target_id: int
    positive: bool
    origin: Origin

    def __str__(self) -> str:
        return f"<Edge {self.id} ({self.label}): {self.source_id} -> {self.target_id}>"

    def json_dict(self) -> Dict[str, str | int | bool]:
        return {
            "type": "edge",
            "id": self.id,
            "source": self.source_id,
            "target": self.target_id,
            "positive": self.positive,
            "label": self.label,
            "origin": self.origin.value,
        }

    __repr__ = __str__


class GraphJSON:

    def __init__(self):
        self.nodes: Dict[int, NodeJSON] = {}
        self.edges: Dict[int, EdgeJSON] = {}
        self._element_id = 0

    def _consume_id(self) -> int:
        self._element_id += 1
        return self._element_id

    def _node_id_exists(self, node_id: int) -> bool:
        return node_id in self.nodes.keys()

    def add_node(self, label: str, origin: Origin) -> NodeJSON:
        node = NodeJSON(self._consume_id(), label, origin)
        self.nodes[node.id] = node
        return node

    def add_edge(
        self,
        source_id: int,
        target_id: int,
        positive: bool,
        origin: Origin,
        label: Optional[str] = None,
    ) -> EdgeJSON:
        if not (self._node_id_exists(source_id) and self._node_id_exists(target_id)):
            raise ValueError("Node IDs not known to the graph")
        edge = EdgeJSON(
            id=self._consume_id(),
            label=label,
            source_id=source_id,
            target_id=target_id,
            positive=positive,
            origin=origin,
        )
        self.edges[edge.id] = edge
        return edge

    def get_node_by_label(self, label: str) -> NodeJSON:
        for node in self.nodes.values():
            if node.label == label:
                return node
        raise KeyError(f"Node with label {label} not found")

    def __str__(self) -> str:
        out = "Nodes:\n"
        for _, node in self.nodes.items():
            out += f"\t- {str(node)}\n"
        out += "Edges:\n"
        for _, edge in self.edges.items():
            out += f"\t- {str(edge)}\n"
        return out

    def json(self) -> str:
        return json.dumps(
            [
                *[n.json_dict() for n in self.nodes.values()],
                *[e.json_dict() for e in self.edges.values()],
            ]
        )

    __repr__ = __str__


def graph_program_to_json(graph_program: str) -> GraphJSON:
    print("INPUT", graph_program)
    graph_json = GraphJSON()
    for rule in graph_program.split("\n"):
        if rule.startswith("node"):
            origin, label = parse_node(rule)
            graph_json.add_node(label, origin)
        elif rule.startswith("edge"):
            origin, label, source_label, target_label, positive = parse_edge(rule)
            source = graph_json.get_node_by_label(source_label)
            target = graph_json.get_node_by_label(target_label)
            graph_json.add_edge(source.id, target.id, positive, origin, label)
        elif rule.startswith("tag"):
            warnings.warn("Found TAG, Ignoring for now")

    print("GRAPH", graph_json)
    return graph_json


def parse_origin(origin_string: str) -> Origin:
    for origin in Origin:
        if origin.value == origin_string.strip():
            return origin
    raise ValueError(f"Unknown origin: {origin_string}")


def parse_positive(positive_string: str) -> bool:
    if positive_string.lower() == "positive":
        return True
    if positive_string.lower() == "negative":
        return False
    raise ValueError(f"Unknown positive: {positive_string}")


def parse_node(node_string: str) -> Tuple[Origin, str]:
    term = clingo.parse_term(node_string.removesuffix("."))
    origin = parse_origin(str(term.arguments[0]))
    label = str(term.arguments[1])
    return origin, label


def parse_edge(edge_string: str) -> Tuple[Origin, str, str, str, bool]:
    print("STRING", edge_string)
    term = clingo.parse_term(edge_string.removesuffix("."))
    origin = parse_origin(str(term.arguments[0]))
    positive = parse_positive(str(term.arguments[1]))
    target_label = str(term.arguments[2].arguments[0])
    source_label = str(term.arguments[2].arguments[1])
    label = str(term.arguments[2])
    return origin, label, source_label, target_label, positive
