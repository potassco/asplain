
_fact(rule(disjunction(H),B)):-
    node(rule(disjunction(H),B),reference), %rule node
    not edge((atom(_), rule(disjunction(H),B)),reference), % no incoming edges (Fact)
    #count{A:edge((rule(disjunction(H),B), atom(A)),reference)} = 1. % single outgoing edge


_abduced_rule(rm, rule(H,B)):-
    _fact(rule(H,B)),
    edge((rule(H,B), atom(A)),reference),
    _abduced(rm,A).


{_abduced(rm,A)} :- _abducible(rm,A).

% Add rules (facts) to make abducible facts true
{_abduced(add,A)} :- _abducible(add,A).
node(rule(disjunction(added(A)),normal(A))):-_abduced(add, A), node(atom(A)).
edge((rule(disjunction(added(A)),normal(A)), atom(A))):-_abduced(add, A), node(atom(A)).


node(atom(A)):-node(atom(A),reference).
node(rule(H,B)):-node(rule(H,B),reference), not _abduced_rule(rm, rule(H, B)).
edge((N1,N2)):-edge((N1,N2),reference), node(N1), node(N2).
edge_attr((N1,N2),A,V):-edge_attr((N1,N2),A,V,reference), node(N1), node(N2).

:- _query(exclude,Atom),  hold(Atom).
:- _query(include,Atom), not hold(Atom).

:~ _distance(N,D,L). [D@L,N]
