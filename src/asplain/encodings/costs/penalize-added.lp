% In the foil program but not in the reference
cost(program_diff(R), 1, 2) :- not program(R, ref), program(R, foil).
