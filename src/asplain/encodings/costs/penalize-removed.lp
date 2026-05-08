% In the reference program but not in the foil
cost(program_diff(R), 1, 2) :- program(R, ref), not program(R, foil).
