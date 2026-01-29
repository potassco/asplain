cost(difference(R), 1, 2):-
        program(R, ref), % Is in the reference
        not program(R, foil). % Is not in the foil

cost(difference(R), 1, 2):-
        not program(R, ref), % Is not in the reference
        program(R, foil). % Is in the foil
