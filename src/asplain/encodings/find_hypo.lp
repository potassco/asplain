
% Any abducible rule can be removed or added.
{abduced(T,R)} :- node_tag(R,abducible(T)).


% Abduced as added need to be included in the hypothetical PG.
% node(rule(disjunction(added(A)),normal(A))):-abduced(add, rule(disjunction(added(A)),normal(A))), node(atom(A)).
% edge((rule(disjunction(added(A)),normal(A)), atom(A))):-abduced(add, rule(disjunction(added(A)),normal(A))), node(atom(A)).


% Gathers all atoms, edges and attributes from the reference PG for nodes present in the hypothetical PG.
node(N):-node(N,reference).
edge((N1,N2)):-edge((N1,N2),reference), node(N1), node(N2).
edge_attr((N1,N2),A,V):-edge_attr((N1,N2),A,V,reference), node(N1), node(N2).

node_tag(N,T):-node_tag(N,T,reference), node(N), T!=disabled, T!=true.


% Abduce add by removing the disabled tag
node_tag(R,disabled):-node_tag(R,disabled,reference), node(R), not abduced(add,R).
node_tag(R,disabled):-node(R,reference), abduced(rm, R).

#include "check_query.lp".
:- fail_query.

% hold(A,reference) :-  node_tag(atom(A),true,reference).
% :-node_tag(N,disabled), node_tag(N,true).
% Adds an optimization based on the distance
used_to_hold(atom(A)):-node_tag(atom(A),true,reference). %Used to simplify writing the distance rules
distance(default, 1, 1). %This rule is added in case no other distance is defined.
:~ distance(N,D,L). [D@L,N]
