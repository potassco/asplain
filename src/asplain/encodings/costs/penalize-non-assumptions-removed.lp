cost(non_assumptions(R), 10, 1):-
        not tag(R,assume(_)), % It was not an assumption
        program(R, ref), % Is in the reference
        not program(R, foil). % Is not in the foil
