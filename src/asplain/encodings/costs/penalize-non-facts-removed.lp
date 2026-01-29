cost(non_fact_removed(R), 1, 3):-
        edge((_,R),_), % Has a body
        program(R, ref), % Is in the reference
        not program(R, foil). % Is not in the foil
