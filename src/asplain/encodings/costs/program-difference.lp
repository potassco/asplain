cost(difference(rule(H,B)), 1, 2):-
        node(reference, rule(H,B)), not tag(reference, rule(H,B), disabled), % Is in the reference
        node(foil, rule(H,B)), tag(foil, rule(H,B), disabled). % Is not in the foil

cost(difference(rule(H,B)), 1, 2):-
        node(reference, rule(H,B)), not tag(reference, rule(H,B), disabled), % Is in the reference
        not node(foil, rule(H,B)). % Is not in the foil

cost(difference(rule(H,B)), 1, 2):-
        node(reference, rule(H,B)), tag(reference, rule(H,B), disabled), % Is not in the reference
        node(foil, rule(H,B)), not tag(foil, rule(H,B), disabled). % Is in the foil
