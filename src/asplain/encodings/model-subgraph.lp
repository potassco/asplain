
% Provides satisfiability based on the program graph
% ------------------------------------------------------
% Similar to the standard ASP semantics encoding, but works on the program graph
% simplified without the sum bodies.

#const graph=reference.

hold(R) :- node(graph, R), R=rule(H,B),
    hold(atom(A)) : edge(graph, positive, (atom(A),R));
    not hold(atom(A)) : edge(graph, negative, (atom(A),R)).

hold(atom(A)) : edge(graph, positive, (rule(disjunction(H),B),atom(A))) :- hold(rule(disjunction(H),B)).
{ hold(atom(A)) : edge(graph, positive, (rule(choice(H),B),atom(A))) } :- hold(rule(choice(H),B)).


node(model(graph), X):-hold(X).
edge(model(graph), positive, (X,Y)):-hold(X), hold(Y), edge(graph, positive, (X,Y)).

#include "show.lp".
