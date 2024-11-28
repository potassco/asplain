% ---- instance
person("Susana",cat). person("Alexander",cat). person("Torsten",dog).
seat((1,1..2)). seat((2,1..2)).

% ---- assumed

assign("Torsten", (1,1)).


1{assign(P,S):seat(S)}1:- person(P,_).

cons(exacly_one) :- person(P,_), assign(P, S), assign(P', S), P' != P.
cons(only_one) :- assign(P,S), assign(P',S), P'>P.
cons(different_type):- assign(P,(T,_)), assign(P',(T,_)), person(P,cat), person(P',dog).
