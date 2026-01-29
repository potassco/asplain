
% Provides satisfiability based on the program graph
% ------------------------------------------------------
% Similar to the standard ASP semantics encoding, but works on the program graph
% simplified without the sum bodies.

#const graph=ref.

model(R,graph) :- node(R), node_type(R, rule(_)), program(R, graph),
    model(A,graph) : edge((A,R)), edge_type((A,R), 1);
    not model(A,graph) : edge((A,R)), edge_type((A,R), 0).

model(A,graph) : edge((R,A)) :- model(R,graph), node_type(R, rule(disjunction)).
{ model(A,graph) : edge((R,A)) } :- model(R,graph), node_type(R, rule(choice)).

#include "show.lp".
#show solved(graph).
