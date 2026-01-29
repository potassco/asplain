from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from clorm import FactBase
from clorm.clingo import ClormControl, ClormModel

from .predicates import (
    Edge,
    Model,
    Node,
    Program,
    Query,
    Tag,
    TagLabel,
    TagRuleFirstOrder,
    TagRuleLocation,
    World,
)
from .processes import ProcessAbducibleRemoved, TagProcess


@dataclass
class GraphNode:
    id: str
    type: str
    models: Set[str]
    programs: Set[str]
    tags: Dict[str, str | bool | Dict[str, str | int]]


@dataclass
class GraphEdge:
    source: str
    target: str
    positive: bool


class Graph:
    def __init__(self, contrastive_program_graph: str) -> None:
        self._graph: str = contrastive_program_graph
        self._facts: Optional[FactBase] = None
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[Tuple[str, str], GraphEdge] = {}
        self._queries: Dict[str, bool] = {}
        self._tag_processes: Set[TagProcess] = {
            ProcessAbducibleRemoved(),
        }

        self.get_facts(self._graph)
        self.compute_nodes()
        self.compute_edges()
        self.compute_queries()

        for node in self._nodes.values():
            print("N", node)
        for edge in self._edges.values():
            print("E", edge)
        for query in self._queries.items():
            print("Q", query)
        print("JSON", self.json())

    def json(
        self,
    ) -> Dict[str, List[Dict[str, str | int | bool]]]:
        json_nodes = []
        for node in self._nodes.values():
            json_node = {
                "type": node.type,
                "id": node.id,
                "models": list(node.models),
                "programs": list(node.programs),
                **node.tags,
            }
            json_nodes.append(json_node)
        json_edges = []
        for edge in self._edges.values():
            json_edge = {
                "positive": edge.positive,
                "source": edge.source,
                "target": edge.target,
            }
            json_edges.append(json_edge)
        json_queries = [
            {"query_atom": atom, "included": inclusion}
            for (atom, inclusion) in self._queries.items()
        ]
        return {"nodes": json_nodes, "edges": json_edges, "query": json_queries}

    def _on_facts_model(self, model: ClormModel) -> None:
        self._facts = model.facts(atoms=True)

    def get_facts(self, program: str) -> None:
        ctl = ClormControl(unifier=[Node, Program, Model, Tag, Edge, Query])
        ctl.add("base", [], program)
        ctl.ground([("base", [])])
        ctl.solve(on_model=self._on_facts_model)

    def compute_nodes(self) -> None:
        if self._facts is None:
            return
        query_nodes = self._facts.query(Node).select(Node)
        for node in query_nodes.all():
            node_id = str(node.element)
            node_type = str(node.type)
            model_worlds = self.get_node_model_worlds(node)
            program_worlds = self.get_node_program_worlds(node)
            tags = self.get_node_tags(node)
            graph_node = GraphNode(
                id=node_id,
                type=node_type,
                models={w.value for w in model_worlds},
                programs={w.value for w in program_worlds},
                tags=tags,
            )
            self._nodes[node_id] = graph_node

    def get_node_model_worlds(self, node: Node) -> Set[World]:
        if self._facts is None:
            return set()
        query_models = (
            self._facts.query(Model).where(Model.node == node.element).select(Model)
        )
        worlds = {model.world for model in query_models.all()}
        return worlds

    def get_node_program_worlds(self, node: Node) -> Set[World]:
        if self._facts is None:
            return set()
        query_models = (
            self._facts.query(Program)
            .where(Program.node == node.element)
            .select(Program)
        )
        worlds = {model.world for model in query_models.all()}
        return worlds

    def get_node_tags(self, node: Node) -> Dict[str, str | bool | Dict[str, str | int]]:
        if self._facts is None:
            return {}
        query_tags = self._facts.query(Tag).where(Tag.node == node.element).select(Tag)
        tags = {}
        for tag in query_tags.all():
            print("TAG", tag, type(tag.tag))
            match tag.tag:
                case str():
                    tags[str(tag.tag)] = True
                case TagLabel():
                    tags["label"] = tag.tag.label  # TODO: Add variables here!
                case TagRuleFirstOrder():
                    tags["first_order"] = tag.tag.first_order
        return tags

    def compute_edges(self) -> None:
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

    def compute_queries(self) -> None:
        if self._facts is None:
            return
        query_query = self._facts.query(Query).select(Query)
        for query in query_query.all():
            query_node = str(query.node)
            self._queries[query_node] = bool(query.included)
