
_fact(rule(disjunction(H),B)):-
    node(rule(disjunction(H),B),reference), %rule node
    not edge((atom(_), rule(disjunction(H),B)),reference), % no incoming edges (Fact)
    #count{A:edge((rule(disjunction(H),B), atom(A)),reference)} = 1. % single outgoing edge


_abduced_rule(rm, rule(H,B)):-
    _fact(rule(H,B)),
    edge((rule(H,B), atom(A)),reference),
    _abduced(rm,A).


:- _query(exclude,Atom),  hold(Atom).
:- _query(include,Atom), not hold(Atom).


{_abduced(rm,A)} :- _abducible(rm,A).

node(atom(A)):-node(atom(A),reference).
node(rule(H,B)):-node(rule(H,B),reference), not _abduced_rule(rm, rule(H, B)).
edge((N1,N2)):-edge((N1,N2),reference), node(N1), node(N2).
edge_attr((N1,N2),A,V):-edge_attr((N1,N2),A,V,reference), node(N1), node(N2).

:~ _distance(N,D,L). [D@L,N]
