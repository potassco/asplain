cost(non_constraint(R), 1, 3):-
        edge((R,_),_), % Has a head
        program(R, ref), % Is in the reference
        not program(R, foil). % Is not in the foil
