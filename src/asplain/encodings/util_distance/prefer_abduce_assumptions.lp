
distance(R, 1, 3) :-
    abduced(_, R), node_tag(R,assume(_)).
distance(R, 1, 4) :-
    abduced(_, R), not node_tag(R,assume(_)).
