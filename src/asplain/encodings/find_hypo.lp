% Create the atoms _abducible_rule/2.
#include "util_preferences/abducible_rules_from_atoms.lp".

% Any abducible rule can be removed or added.
{_abduced(rm,R)} :- _abducible_rule(rm,R).
{_abduced(add,R)} :- _abducible_rule(add,R).

_abduced_atom(add,A) :- _abduced(add, rule(disjunction(added(A)),normal(A))).
_abduced_atom(rm,A) :- _abduced(rm, rule(disjunction(H),B)), _fact(rule(disjunction(H),B)), edge((rule(disjunction(H),B), atom(A)),reference).

% Abduced as added need to be included in the hypothetical PG.
node(rule(disjunction(added(A)),normal(A))):-_abduced(add, rule(disjunction(added(A)),normal(A))), node(atom(A)).
edge((rule(disjunction(added(A)),normal(A)), atom(A))):-_abduced(add, rule(disjunction(added(A)),normal(A))), node(atom(A)).


% Gathers all atoms, edges and attributes from he reference PG for nodes present in the hypothetical PG.
node(atom(A)):-node(atom(A),reference).
edge((N1,N2)):-edge((N1,N2),reference), node(N1), node(N2).
edge_attr((N1,N2),A,V):-edge_attr((N1,N2),A,V,reference), node(N1), node(N2).

% Gathers all rules unless a rule is abduced for removal.
node(rule(H,B)):-node(rule(H,B),reference), not _abduced(rm, rule(H, B)).

% Makes sure that the query holds in the hypothetical model.
:- _query(exclude,Atom),  hold(Atom).
:- _query(include,Atom), not hold(Atom).

% Adds an optimization based on the distance
_distance(default, 1, 1). %This rule is added in case no other distance is defined.
:~ _distance(N,D,L). [D@L,N]
