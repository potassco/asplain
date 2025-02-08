#program base.
% person("Susana",cat).
_rule(1,"person(\"Susana\",cat).").
_sup(1,World,person("Susana",cat),()) :- world(World).
% person("Alexander",cat).
_rule(2,"person(\"Alexander\",cat).").
_sup(2,World,person("Alexander",cat),()) :- world(World).
% person("Torsten",dog).
_rule(3,"person(\"Torsten\",dog).").
_sup(3,World,person("Torsten",dog),()) :- world(World).
% seat((1,(1..2))).
_rule(4,"seat((1,(1..2))).").
_sup(4,World,seat((1,(1..2))),()) :- world(World).
% seat((2,(1..2))).
_rule(5,"seat((2,(1..2))).").
_sup(5,World,seat((2,(1..2))),()) :- world(World).
% ---- encoding
% 1 <= { assign(P,S): seat(S) } <= 1 :- person(P,A).
_rule(6,"1 <= { assign(P,S): seat(S) } <= 1 :- person(P,A).").
_sup(6,World,assign(P,S),(A,P,S)) :- world(World); _model(World,person(P,A)); _model(World,seat(S)).
_depends(_sup(6,World,assign(P,S),(A,P,S)),(person(P,A);seat(S))) :- _sup(6,World,assign(P,S),(A,P,S)).
_rule(7,"#false :- 1 < #count { assign(P,S): assign(P,S), seat(S) }; person(P,A).").
_sup_constraint(7,(A,P)) :- world(World); 1 < #count { assign(P,S): _model(_,assign(P,S)), _model(_,seat(S)) }; _model(_,person(P,A)).
_constraints(_sup_constraint(7,(A,P)),person(P,A)) :- _sup_constraint(7,(A,P)).
_constraints(_sup_constraint(7,(A,P)),(assign(P,S);seat(S))) :- _model(_,assign(P,S)); _model(_,seat(S)); _sup_constraint(7,(A,P)).
_rule(8,"#false :- 1 > #count { assign(P,S): assign(P,S), seat(S) }; person(P,A).").
_sup_constraint(8,(A,P)) :- world(World); 1 > #count { assign(P,S): _model(_,assign(P,S)), _model(_,seat(S)) }; _model(_,person(P,A)).
_constraints(_sup_constraint(8,(A,P)),person(P,A)) :- _sup_constraint(8,(A,P)).
_constraints(_sup_constraint(8,(A,P)),(assign(P,S);seat(S))) :- _model(_,assign(P,S)); _model(_,seat(S)); _sup_constraint(8,(A,P)).
% #false :- assign(P,S); assign(P',S); P' > P.
_rule(9,"#false :- assign(P,S); assign(P',S); P' > P.").
_sup_constraint(9,(P,P',S)) :- world(World); _model(_,assign(P,S)); _model(_,assign(P',S)); P' > P.
_constraints(_sup_constraint(9,(P,P',S)),(assign(P,S);assign(P',S))) :- _sup_constraint(9,(P,P',S)).
% #false :- assign(P,(T,C)); assign(P',(T,C')); person(P,cat); person(P',dog).
_rule(10,"#false :- assign(P,(T,C)); assign(P',(T,C')); person(P,cat); person(P',dog).").
_sup_constraint(10,(C,C',P,P',T)) :- world(World); _model(_,assign(P,(T,C))); _model(_,assign(P',(T,C'))); _model(_,person(P,cat)); _model(_,person(P',dog)).
_constraints(_sup_constraint(10,(C,C',P,P',T)),(assign(P,(T,C));assign(P',(T,C'));person(P,cat);person(P',dog))) :- _sup_constraint(10,(C,C',P,P',T)).
% ---- assumed
% assign("Torsten",(1,1)).
_rule(11,"assign(\"Torsten\",(1,1)).").
_sup(11,World,assign("Torsten",(1,1)),()) :- world(World).