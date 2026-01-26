
% Provides satisfiability based on the program graph
% ------------------------------------------------------
% Similar to the standard ASP semantics encoding, but works on the program graph
% simplified without the sum bodies.

#const graph=ref.

hold(R) :- node(R), node_type(R, rule(_)), p_member(R, graph),
    hold(A) : edge((A,R)), edge_type((A,R), 1);
    not hold(A) : edge((A,R)), edge_type((A,R), 0).

hold(A) : edge((R,A)) :- hold(R), node_type(R, rule(disjunction)).
{ hold(A) : edge((R,A)) } :- hold(R), node_type(R, rule(choice)).

m_member(N, graph) :- hold(N).

#include "show.lp".
