% In the reference model but not in the foil
cost(model_diff(R), 1, 2) :- model(R, ref), not model(R, foil).

% In the foil model but not in the reference
cost(model_diff(R), 1, 2) :- not model(R, ref), model(R, foil).
