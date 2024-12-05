%===== Abducibles

_abducible((rm;add),r(a)).
_abducible((rm;add),r(b)).
_abducible((rm;add),s(a,b)).
_abducible((rm;add),s(b,a)).

%===== Distance
%      It adds a penalty of 1 for each atom that is abduced.

_distance(Atom, 1, 1) :-
    _abduced(_, Atom).
