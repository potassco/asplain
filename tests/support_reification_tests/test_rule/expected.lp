#program base.
% punish(P) :- drive(P); alcohol(P,A); A > 30; person(P).
_rule(1,"punish(P) :- drive(P); alcohol(P,A); A > 30; person(P).").
_sup(1,World,punish(P),(A,P)) :- world(World); _model(World,drive(P)); _model(World,alcohol(P,A)); A > 30; _model(World,person(P)).
_depends(_sup(1,World,punish(P),(A,P)),(drive(P);alcohol(P,A);person(P))) :- _sup(1,World,punish(P),(A,P)).