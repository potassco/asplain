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
_sup(6,World,assign(P,S),(A,P)) :- world(World); _model(World,person(P,A)).
_depends(_sup(6,World,assign(P,S),(A,P)),(person(P,A);seat(S))) :- _sup(6,World,assign(P,S),(A,P)).
% error :- person(P,A); assign(P,S); assign(P',S); P' != P.
_sup(7,World,error,(A,P,P',S)) :- world(World); _model(World,person(P,A)); _model(World,assign(P,S)); _model(World,assign(P',S)); P' != P.
_depends(_sup(7,World,error,(A,P,P',S)),(person(P,A);assign(P,S);assign(P',S))) :- _sup(7,World,error,(A,P,P',S)).
% error :- person(P,A); assign(P,S); assign(P',S); P' != P.
_sup(8,World,error,(A,P,P',S)) :- world(World); _model(World,person(P,A)); _model(World,assign(P,S)); _model(World,assign(P',S)); P' != P.
_depends(_sup(8,World,error,(A,P,P',S)),(person(P,A);assign(P,S);assign(P',S))) :- _sup(8,World,error,(A,P,P',S)).
% error :- assign(P,S); assign(P',S); P' > P.
_sup(9,World,error,(P,P',S)) :- world(World); _model(World,assign(P,S)); _model(World,assign(P',S)); P' > P.
_depends(_sup(9,World,error,(P,P',S)),(assign(P,S);assign(P',S))) :- _sup(9,World,error,(P,P',S)).
% error :- assign(P,(T,C)); assign(P',(T,C')); person(P,cat); person(P',dog).
_sup(10,World,error,(C,C',P,P',T)) :- world(World); _model(World,assign(P,(T,C))); _model(World,assign(P',(T,C'))); _model(World,person(P,cat)); _model(World,person(P',dog)).
_depends(_sup(10,World,error,(C,C',P,P',T)),(assign(P,(T,C));assign(P',(T,C'));person(P,cat);person(P',dog))) :- _sup(10,World,error,(C,C',P,P',T)).
% #false :- error.
% ---- assumed
% assign("Torsten",(1,1)).
_sup(11,World,assign("Torsten",(1,1)),()) :- world(World).