person("Susana",cat). person("Alexander",cat). person("Torsten",dog).
seat((1,1..2)). seat((2,1..2)).

% ---- encoding

1{assign(P,S):seat(S)}1:- person(P,A).


:- assign(P,S), assign(P',S), P'>P.
:- assign(P,(T,C)), assign(P',(T,C')), person(P,cat), person(P',dog).

% ---- assumed

assign("Torsten", (1,1)).
