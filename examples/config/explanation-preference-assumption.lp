% %%% _abducible(A)
% % A is an abducible atom
% % If A is true in the model then it may be removed for the contrastive explanation.
% % If A is false in the model then it may be added for the contrastive explanation


_distance(Atom, 1, 2) :-
    _abduced(_, Atom), _input(_,Atom).
_distance(Atom, 1, 1) :-
    _abduced(_, Atom), not _input(_,Atom).


_domain(variable(V,T)):- _model(real,variable(V,T)).
_domain(domain(T,D)):- _model(real,domain(T,D)).

_abducible(rm,value("frontWheel",18)).
_abducible(rm,value("rearWheel",18)).
_abducible(rm,value("color","Red")).
