cost(model_diff(R), 1, 2):-
        model(R, ref), % Is in the reference
        not model(R, foil). % Is not in the foil

cost(model_diff(R), 1, 2):-
        not model(R, ref), % Is not in the reference
        model(R, foil). % Is in the foil
