cost(program_diff(R), 1, 2):-
        program(R, ref), % Is in the reference
        not program(R, foil). % Is not in the foil
