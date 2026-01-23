cost(difference(rule(H,B)), 1, 2):-
        node(reference, rule(H,B)), % Is in the reference
        not node(foil, rule(H,B)). % Is not in the foil

cost(difference(rule(H,B)), 1, 2):-
        not node(reference, rule(H,B)), % Is not in the reference
        node(foil, rule(H,B)). % Is in the foil
