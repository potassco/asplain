cost(difference(R), 1, 3):-
        node(reference, R), % Is in the reference
        not node(foil, R), % Is not in the foil
        not tag(reference, R, assume(_)). % Not an assumption
