%===== Abducibles
_abducible((rm;add),d).
_abducible((rm;add),h).

%===== Distance
_distance(Atom, 1, 1) :-
    _abduced(_, Atom).
