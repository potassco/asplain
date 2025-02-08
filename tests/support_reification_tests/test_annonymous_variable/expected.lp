#program base.
% person(X) :- parent(X,_Annon_1).
_rule(1,"person(X) :- parent(X,_Annon_1).").
_sup(1,World,person(X),(X,_Annon_1)) :- world(World); _model(World,parent(X,_Annon_1)).
_depends(_sup(1,World,person(X),(X,_Annon_1)),parent(X,_Annon_1)) :- _sup(1,World,person(X),(X,_Annon_1)).
% person(X) :- parent(_Annon_2,X).
_rule(2,"person(X) :- parent(_Annon_2,X).").
_sup(2,World,person(X),(X,_Annon_2)) :- world(World); _model(World,parent(_Annon_2,X)).
_depends(_sup(2,World,person(X),(X,_Annon_2)),parent(_Annon_2,X)) :- _sup(2,World,person(X),(X,_Annon_2)).