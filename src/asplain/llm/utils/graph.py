"""
Graph utilities for generating the explanation graph representation for the LLM
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from clorm import FactBase
from clorm._clingo import ClormControl, ClormModel

from .predicates import (
    Edge,
    Fired,
    Model,
    Node,
    Program,
    Query,
    Tag,
    TagLabel,
    TagRuleFirstOrder,
)


@dataclass
class GraphNode:
    """Node of the explanation graph"""

    id: str
    type: str
    models: Set[str]
    programs: Set[str]
    tags: Dict[str, str | bool | Dict[str, str | int]]
    fired: bool


@dataclass
class GraphEdge:
    """Edge of the explanation graph"""

    source: str
    target: str
    positive: bool


class Graph:
    """Representation of the explanation graph for the LLM"""

    def __init__(self, contrastive_program_graph: str) -> None:
        self._graph: str = contrastive_program_graph
        self._facts: Optional[FactBase] = None
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[Tuple[str, str], GraphEdge] = {}
        self._queries: Dict[str, bool] = {}

        self._get_facts(self._graph)
        self._compute_nodes()
        self._compute_edges()
        self._compute_queries()

    def json(
        self,
    ) -> Dict[str, List[Dict[str, str | int | bool]]]:
        """
        A JSON representation of the explanation graph
        Returns:
            A JSON representation of the explanation graph as a python dictionary
        """

        json_nodes = []
        for node in self._nodes.values():
            json_node = {
                "type": node.type,
                "id": node.id,
                "models": list(node.models),
                "programs": list(node.programs),
                **node.tags,
            }
            if node.fired:
                json_node["fired"] = True
            json_nodes.append(json_node)
        json_edges = []
        for edge in self._edges.values():
            json_edge = {
                "type": ["negative", "positive"][edge.positive],
                "source": edge.source,
                "target": edge.target,
            }
            json_edges.append(json_edge)
        json_queries = [
            {"query_atom": atom, "type": "positive" if inclusion else "negative"}
            for (atom, inclusion) in self._queries.items()
        ]
        return {"nodes": json_nodes, "edges": json_edges, "query": json_queries}

    def _on_facts_model(self, model: ClormModel) -> None:
        self._facts = model.facts(atoms=True)

    def _get_facts(self, program: str) -> None:
        ctl = ClormControl(unifier=[Node, Program, Model, Tag, Edge, Query, Fired])
        ctl.add("base", [], program)
        ctl.ground([("base", [])])
        ctl.solve(on_model=self._on_facts_model)

    def _compute_nodes(self) -> None:
        if self._facts is None:
            return
        query_nodes = self._facts.query(Node).select(Node)
        nodes = {}
        for node in query_nodes.all():
            nodes[str(node.element)] = {
                "type": str(node.type),
                "models": set(),
                "programs": set(),
                "tags": {},
                "fired": False,
            }

        self._set_node_model_worlds(nodes)
        self._set_node_program_worlds(nodes)
        self._set_node_tags(nodes)
        self._set_node_fired(nodes)
        for node_id, node in nodes.items():
            graph_node = GraphNode(
                id=node_id,
                type=node["type"],
                models=node["models"],
                programs=node["programs"],
                tags=node["tags"],
                fired=node["fired"],
            )
            self._nodes[node_id] = graph_node

    def _set_node_fired(self, nodes) -> None:
        if self._facts is None:
            return
        for qf in self._facts.query(Fired).all():
            nodes[str(qf.node)]["fired"] = True

    def _set_node_model_worlds(self, nodes) -> None:
        if self._facts is None:
            return
        for m in self._facts.query(Model).all():
            nodes[str(m.node)]["models"].add(m.world)

    def _set_node_program_worlds(self, nodes) -> None:
        if self._facts is None:
            return
        for p in self._facts.query(Program).all():
            nodes[str(p.node)]["programs"].add(p.world)

    def _set_node_tags(self, nodes) -> None:
        if self._facts is None:
            return
        for tag in self._facts.query(Tag).all():
            if str(tag.tag) == "shown":
                continue
            match tag.tag:
                case str():
                    nodes[str(tag.node)]["tags"][str(tag.tag)] = True
                case TagLabel():
                    nodes[str(tag.node)]["tags"]["label"] = tag.tag.label.format(
                        *[str(a) for a in tag.tag.variables.symbol.arguments]
                    )
                case TagRuleFirstOrder():
                    nodes[str(tag.node)]["tags"]["first_order"] = tag.tag.first_order

    def _compute_edges(self) -> None:
        if self._facts is None:
            return
        query_edges = self._facts.query(Edge).select(Edge)
        for edge in query_edges.all():
            edge_id = (str(edge.nodes.source), str(edge.nodes.target))
            graph_edge = GraphEdge(
                source=str(edge.nodes.source),
                target=str(edge.nodes.target),
                positive=bool(edge.positive),
            )
            self._edges[edge_id] = graph_edge

    def _compute_queries(self) -> None:
        if self._facts is None:
            return
        query_query = self._facts.query(Query).select(Query)
        for query in query_query.all():
            query_node = str(query.node)
            self._queries[query_node] = bool(query.included)
