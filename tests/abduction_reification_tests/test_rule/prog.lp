punish(P) :- drive(P), alcohol(P),  person(P).
punish(P) :- resist(P), person(P).

sentence(P, prison) :- punish(P).
sentence(P, innocent) :- person(P), not punish(P).