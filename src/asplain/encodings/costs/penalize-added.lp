cost(program_diff(R), 1, 2):-
        not program(R, ref), % Is not in the reference
        program(R, foil). % Is in the foil
