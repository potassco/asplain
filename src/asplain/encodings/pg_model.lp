
% Provides satisfiability based on the program graph
% ------------------------------------------------------


% Mimics literal_tuple
_my_literal_tuple(B):-node(rule(H,normal(B))).
_my_literal_tuple(B,A,pos):-edge_attr((atom(A),rule(H,normal(B))), type, positive).
_my_literal_tuple(B,A,neg):-edge_attr((atom(A),rule(H,normal(B))), type, negative).

% Mimics weighted_literal_tuple
_my_w_literal_tuple(B,A,pos,W):-
    edge_attr((atom(A),rule(H,sum(B,G))), weight, W),
    edge_attr((atom(A),rule(H,sum(B,G))), type, positive).
_my_w_literal_tuple(B,A,neg,W):-
    edge_attr((atom(A),rule(H,sum(B,G))), weight, W),
    edge_attr((atom(A),rule(H,sum(B,G))), type, negative).


% Satisfiable based on program graph
conjunction(B) :- _my_literal_tuple(B),
    hold(A) : _my_literal_tuple(B, A, pos);
    not hold(A) : _my_literal_tuple(B, A, neg).

body(normal(B)) :- node(rule(H,normal(B))), conjunction(B).
body(sum(B,G)) :- node(rule(H,sum(B,G))),
    #sum { W,A : hold(A), _my_w_literal_tuple(B, A, pos, W) ;
           W,A : not hold(A), _my_w_literal_tuple(B, A, neg, W) } >= G.

hold(A) : edge((rule(disjunction(H),B),atom(A))) :- node(rule(disjunction(H),B)), body(B), not node_tag(rule(disjunction(H),B),disabled).
{ hold(A) : edge((rule(choice(H),B),atom(A))) } :- node(rule(choice(H),B)), body(B), not node_tag(rule(choice(H),B),disabled).
