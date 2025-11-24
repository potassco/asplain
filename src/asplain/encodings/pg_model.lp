
% Provides satisfiability based on the program graph
% ------------------------------------------------------
% Similar to the standard ASP semantics encoding, but works on the program graph
% simplified without the sum bodies.

body(B) :- node(rule(H,B)),
    hold(atom(A)) : edge_attr((atom(A),rule(y)), type, positive);
    not hold(atom(A)) : edge_attr((atom(A),rule(H,B)), type, negative).

hold(rule(H,B)):-node(rule(H,B)), body(B), not node_tag(rule(H,B),disabled).

hold(atom(A)) : edge((rule(disjunction(H),B),atom(A))) :- hold(rule(disjunction(H),B)).
{ hold(atom(A)) : edge((rule(choice(H),B),atom(A))) } :- hold(rule(choice(H),B)).
