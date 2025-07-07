
_distance(R, 1, 3) :-
    _abduced(_, R), _cons_single(R).
_distance(R, 1, 4) :-
    _abduced(_, R), not _cons_single(R).
