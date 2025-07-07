% Predicates to define different types of rules from the structure of the program graph.

_fact(rule(disjunction(H),B)):-
    node(rule(disjunction(H),B),reference), %rule node
    not edge((atom(_), rule(disjunction(H),B)),reference), % no incoming edges (Fact)
    #count{A:edge((rule(disjunction(H),B), atom(A)),reference)} = 1. % single outgoing edge

_cons(rule(disjunction(H),B)):-
    node(rule(disjunction(H),B),reference), %rule node
    not edge((rule(disjunction(H),B),atom(_)),reference). % no outgoing edges


% Constraints with a single atom, usually are due to assumptions.
_cons_single(rule(disjunction(H),B)):-
    _cons(rule(disjunction(H),B)),
    #count{A:edge((atom(A),rule(disjunction(H),B)),reference)} = 1. %single incoming edge
