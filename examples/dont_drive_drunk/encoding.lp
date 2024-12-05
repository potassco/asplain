% The original program.

person(gabriel).
person(clare).

drive(gabriel).
alcohol(gabriel).

drive(clare).

punish(P) :- drive(P), alcohol(P),  person(P).
punish(P) :- resist(P), person(P).

sentence(P, prison) :- punish(P).
sentence(P, innocent) :- person(P), not punish(P).
