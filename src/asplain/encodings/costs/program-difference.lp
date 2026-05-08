% In the reference program but not in the foil
cost(program_diff(R), 1, 2) :- program(R, ref), not program(R, foil).

% In the foil program but not in the reference
cost(program_diff(R), 1, 2) :- not program(R, ref), program(R, foil).
