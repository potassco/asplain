% Rule is in the reference program but not in the foil and was not an assumption
cost(non_assumptions(R), 10, 1) :- not tag(R,assume(_)), program(R, ref), not program(R, foil).
