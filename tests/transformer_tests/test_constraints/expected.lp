#program base.
% person("Susana",cat).
_sup(1,World,person("Susana",cat),()) :- world(World).
% person("Alexander",cat).
_sup(2,World,person("Alexander",cat),()) :- world(World).
% person("Torsten",dog).
_sup(3,World,person("Torsten",dog),()) :- world(World).
% seat((1,(1..2))).
_sup(4,World,seat((1,(1..2))),()) :- world(World).
% seat((2,(1..2))).
_sup(5,World,seat((2,(1..2))),()) :- world(World).
% ---- encoding
% 1 <= { assign(P,S): seat(S) } <= 1 :- person(P,A).
_sup(6,World,assign(P,S),(A,P,S)) :- world(World); _model(World,person(P,A)); _model(World,seat(S)).
_depends(_sup(6,World,assign(P,S),(A,P,S)),(person(P,A);seat(S))) :- _sup(6,World,assign(P,S),(A,P,S)).
% #false :- assign(P,S); assign(P',S); P' > P.
_constraints((1,(P,P',S)),(assign(P,S);assign(P',S))) :- _model(_,assign(P,S)); _model(_,assign(P',S)); P' > P.
% #false :- assign(P,(T,C)); assign(P',(T,C')); person(P,cat); person(P',dog).
_constraints((2,(C,C',P,P',T)),(assign(P,(T,C));assign(P',(T,C'));person(P,cat);person(P',dog))) :- _model(_,assign(P,(T,C))); _model(_,assign(P',(T,C'))); _model(_,person(P,cat)); _model(_,person(P',dog)).
% ---- assumed
% assign("Torsten",(1,1)).
_sup(7,World,assign("Torsten",(1,1)),()) :- world(World).