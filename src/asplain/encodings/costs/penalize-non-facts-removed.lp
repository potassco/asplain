% Rule is in the reference program but not in the foil and has a body
cost(non_fact_removed(R), 1, 3) :- edge((_,R),_), program(R, ref), not program(R, foil).
