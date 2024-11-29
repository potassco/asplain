% ---- instance
person("Susana",cat). person("Alexander",cat). person("Torsten",dog).
seat((1,1..2)). seat((2,1..2)).

% ---- encoding

1{assign(P,S):seat(S)}1:- person(P,A).

error  :- person(P,A), assign(P, S), assign(P', S), P' != P.
error  :- person(P,A), assign(P, S), assign(P', S), P' != P.
error  :- assign(P,S), assign(P',S), P'>P.
error  :- assign(P,(T,C)), assign(P',(T,C')), person(P,cat), person(P',dog).

:- error.

% ---- assumed

assign("Torsten", (1,1)).
