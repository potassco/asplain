% Defines the preference for the explanation.

%===== Abducibles
%     In this case, atoms `d` and `h` can be either removed or added from the reference model
%     to find the hypothetical model


%===== Distance
%      It adds a penalty of 1 for each atom that is abduced.

_distance(Atom, 1, 2) :-
    _abduced(_, Atom), _input(_,Atom).
_distance(Atom, 1, 1) :-
    _abduced(_, Atom), not _input(_,Atom).

_domain(time(T)):- _model(real,time(T)).
