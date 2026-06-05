% Rule is in the referece program but not in the foil and has a head
cost(non_constraint(R), 1, 3):- edge((R,_),_), program(R, ref), not program(R, foil).
